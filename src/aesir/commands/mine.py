#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/mine.py
# VERSION: 	   0.4.1
# CREATED: 	   2023-12-01 05:31
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
from aesir.types import BlockchainInfo, LNDInfo, NewAddress


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
    filter(
      lambda container: match(r"aesir-lnd|aesir-ping|aesir-pong", container.name),
      aesir_containers,
    )
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

  with Live(pane, refresh_per_second=4, transient=True):
    pane["containers"].update(Panel(Text("\n".join(container_names)), title="containers"))
    while True:
      ### Update ###
      blockchain_info: BlockchainInfo = TypeAdapter(BlockchainInfo).validate_json(
        bitcoind.exec_run(
          """
          bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir getblockchaininfo
          """
        ).output
      )

      ### Initiate parameters ###
      lnd_infos: List[LNDInfo] = []
      lnd_names: List[str] = []

      ## Fetch LNDInfo from LND containers ###
      for container in lnd_containers:
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
        lnd_infos.append(lnd_info)
        lnd_names.append(container.name)

      ### Draw ###
      body_table: Table = Table(expand=True, show_lines=True)
      body_table.add_column("Name", justify="left", style="green")
      body_table.add_column("Nodekey", justify="left", style="cyan")
      body_table.add_column("Channels")
      body_table.add_column("Peers")
      body_table.add_column("Height")
      body_table.add_column("Synced?", justify="right")
      for i, lnd_info in enumerate(lnd_infos):
        body_table.add_row(
          lnd_names[i],
          "\n".join(
            lnd_info.identity_pubkey[c : c + 11]
            for c in range(0, len(lnd_info.identity_pubkey), 11)
          ),
          f"{lnd_info.num_active_channels}",
          f"{lnd_info.num_peers}",
          f"{lnd_info.block_height}",
          ("[red]false", "[green]true")[lnd_info.synced_to_chain],
        )
      pane["body"].update(body_table)
      pane["footer"].update(
        Panel(
          Text.assemble(
            ("Chain: ", "bright_magenta bold"),
            blockchain_info.chain.ljust(9),
            ("Blocks: ", "green bold"),
            f"{blockchain_info.blocks}".ljust(8),
            ("Size: ", "blue bold"),
            f"{blockchain_info.size_on_disk}".ljust(10),
            ("Time: ", "cyan bold"),
            f"{blockchain_info.time}".rjust(10),
          )
        )
      )


__all__ = ["mine"]
