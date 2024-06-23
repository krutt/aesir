#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/mine.py
# VERSION:     0.4.3
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from typing import List

### Third-party packages ###
from apscheduler.schedulers.background import BackgroundScheduler
from blessed import Terminal
from blessed.keyboard import Keystroke
from click import argument, command
from docker import DockerClient, from_env
from docker.errors import DockerException, NotFound
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich import print as rich_print
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

### Local modules ###
from aesir.types import BlockchainInfo, LNDInfo, NewAddress, MempoolInfo


@command
@argument("blockcount", default=1, type=int)
@argument("blocktime", default=5, type=int)
def mine(blockcount: int, blocktime: int) -> None:
  """Scheduled mining with "blockcount" and "blocktime"."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to daemon.")
    return

  ### Retrieve bitcoind container ###
  bitcoind: Container
  try:
    bitcoind = client.containers.get("aesir-bitcoind")
  except NotFound:
    rich_print('[red bold]Unable to find "aesir-bitcoind" container.')
    return

  ### Retrieve other containers ###
  aesir_containers: List[Container] = list(
    filter(lambda container: match(r"aesir-*", container.name), reversed(client.containers.list()))
  )
  container_names: List[str] = list(map(lambda container: container.name, aesir_containers))
  lnd_containers: List[Container] = list(
    filter(lambda container: match(r"aesir-(lnd|ping|pong)", container.name), aesir_containers)
  )

  ### Generate treasury addresses as mining destinations ###
  treasuries: List[str] = []
  for container in track(lnd_containers, "Generate mining treasuries:".ljust(42)):
    new_address: NewAddress = TypeAdapter(NewAddress).validate_json(
      container.exec_run(
        """
        lncli
          --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
          --rpcserver=localhost:10001
          --tlscertpath=/home/lnd/.lnd/tls.cert
        newaddress p2wkh
        """
      ).output
    )
    treasuries.append(new_address.address)

  ### Set up mining schedule using command arguments ###
  scheduler: BackgroundScheduler = BackgroundScheduler()
  for address in treasuries:
    scheduler.add_job(
      bitcoind.exec_run,
      "interval",
      [
        """
        bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir generatetoaddress %d %s
        """
        % (blockcount, address)
      ],
      seconds=blocktime,
    )
  scheduler.start()

  ### Initiate Terminal instance ###
  terminal: Terminal = Terminal()

  ### Set up dashboard layout ###
  pane: Layout = Layout()
  sidebar: Layout = Layout(size=24)
  containers: Layout = Layout(name="containers", size=20)
  main: Layout = Layout(size=72)
  body: Layout = Layout(name="body", minimum_size=4, ratio=8, size=17)
  footer: Layout = Layout(name="footer", size=3)
  pane.split_row(sidebar, main)
  main.split_column(body, footer)
  sidebar.split_column(containers)

  container_index: int = 0
  with terminal.cbreak(), terminal.hidden_cursor(), Live(
    pane, refresh_per_second=4, transient=True
  ):
    try:
      while True:
        ### Process input key ###
        keystroke: Keystroke = terminal.inkey(timeout=0.25)
        if keystroke.code == terminal.KEY_UP and container_index > 0:
          container_index -= 1
        elif keystroke.code == terminal.KEY_DOWN and container_index < len(container_names) - 1:
          container_index += 1
        elif keystroke in {"Q", "q"}:
          raise StopIteration

        container_rows: str = ""
        if container_index > 0:
          container_rows = "\n".join(container_names[:container_index])
          container_rows += f"\n[reverse]{container_names[container_index]}[reset]\n"
        else:
          container_rows = f"[reverse]{container_names[container_index]}[reset]\n"
        if container_index < len(container_names) - 1:
          container_rows += "\n".join(container_names[container_index + 1 :])
        pane["containers"].update(Panel(container_rows, title="containers"))

        container_name: str = container_names[container_index]
        body_table: Table = Table(expand=True, show_lines=True)
        body_table.add_column(container_name, "dark_sea_green bold")
        if match(r"aesir-(bitcoind)", container_name):
          blockchain_info: BlockchainInfo = TypeAdapter(BlockchainInfo).validate_json(
            bitcoind.exec_run(
              """
              bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir getblockchaininfo
              """
            ).output
          )
          mempool_info: MempoolInfo = TypeAdapter(MempoolInfo).validate_json(
            bitcoind.exec_run(
              """
              bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir getmempoolinfo
              """
            ).output
          )
          body_table.add_row(
            Text.assemble(
              f"\n{ 'Blockchain information:'.ljust(20) }\n",
              ("Chain: ", "bright_magenta bold"),
              blockchain_info.chain.ljust(9),
              ("Blocks: ", "green bold"),
              f"{blockchain_info.blocks}".ljust(8),
              ("Size: ", "blue bold"),
              f"{blockchain_info.size_on_disk}".ljust(10),
              ("Time: ", "cyan bold"),
              f"{blockchain_info.time}".rjust(10),
              "\n",
            )
          )
          body_table.add_row(
            Text.assemble(
              "\n",
              ("Mempool information".ljust(19), "bold"),
              "\n".ljust(19),
              ("Fees:".ljust(15), "green bold"),
              f"{mempool_info.total_fee}".rjust(15),
              "\n".ljust(19),
              ("Transactions:".ljust(15), "cyan bold"),
              f"{mempool_info.txn_count}".rjust(15),
              "\n".ljust(19),
              ("Size:".ljust(15), "blue bold"),
              f"{mempool_info.txn_bytes}".rjust(15),
              "\n".ljust(19),
              ("Loaded?:".ljust(15), "bright_magenta bold"),
              ("true".rjust(15), "green") if mempool_info.loaded else ("false".rjust(15), "red"),
              "\n".ljust(19),
              ("Usage:".ljust(15), "light_coral bold"),
              f"{mempool_info.usage}".rjust(15),
              "\n",
            )
          )
        elif match(r"aesir-(lnd|ping|pong)", container_name):
          container = next(
            filter(
              lambda container: container.name == container_name,
              aesir_containers,
            )
          )
          lnd_info: LNDInfo = TypeAdapter(LNDInfo).validate_json(
            container.exec_run(
              """
              lncli
                --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
                --rpcserver=localhost:10001
                --tlscertpath=/home/lnd/.lnd/tls.cert
              getinfo
              """
            ).output
          )
          body_table.add_row(
            Text.assemble(
              "\n\n\n",
              ("Nodekey:\n", "light_coral bold"),
              lnd_info.identity_pubkey,
              "\n",
              "\n".ljust(19),
              ("Channels:".ljust(10), "green bold"),
              str(lnd_info.num_active_channels).rjust(20),
              "\n".ljust(19),
              ("Peers:".ljust(10), "cyan bold"),
              str(lnd_info.num_peers).rjust(20),
              "\n".ljust(19),
              ("Blocks:".ljust(10), "rosy_brown bold"),
              str(lnd_info.block_height).rjust(20),
              "\n".ljust(19),
              ("Synced?:".ljust(10), "steel_blue bold"),
              ("true".rjust(20), "green")
              if lnd_info.synced_to_chain
              else ("false".rjust(20), "red"),
              "\n\n\n",
            )
          )
        pane["body"].update(body_table)
        pane["footer"].update(
          Panel(
            Text.assemble(
              "Select:".rjust(16),
              (" ↑↓ ", "bright_magenta bold"),
              " " * 20,
              "Exit:".rjust(16),
              ("  Q ", "red bold"),
            )
          )
        )
    except StopIteration:
      print("Valhalla!")


__all__ = ["mine"]
