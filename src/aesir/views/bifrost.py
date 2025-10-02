#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/bifrost.py
# VERSION:     0.5.3
# CREATED:     2024-06-25 19:43
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from typing import ClassVar

### Third-party packages ###
from blessed import Terminal
from blessed.keyboard import Keystroke
from curses import KEY_DOWN, KEY_UP
from docker.models.containers import Container
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr, TypeAdapter
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

### Local modules ###
from aesir.types import BlockchainInfo, Features, JsonrpcResponse, LNDInfo, MempoolInfo, OrdStatus


class Bifrost(BaseModel):
  model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)
  bitcoind: Container
  container_index: StrictInt = 0
  container_names: list[StrictStr] = []
  containers: list[Container] = []

  ### Split layouts ###
  body: ClassVar[Layout] = Layout(name="body", minimum_size=4, ratio=8, size=17)
  footer: ClassVar[Layout] = Layout(name="footer", size=3)
  main: ClassVar[Layout] = Layout(size=72)
  pane: ClassVar[Layout] = Layout()
  realms: ClassVar[Layout] = Layout(name="realms", size=20)
  sidebar: ClassVar[Layout] = Layout(size=24)

  ### Terminal ###
  terminal: ClassVar[Terminal] = Terminal()

  def model_post_init(self, _) -> None:  # type: ignore[no-untyped-def]
    self.pane.split_row(self.sidebar, self.main)
    self.main.split_column(self.body, self.footer)
    self.sidebar.split_column(self.realms)

  def display(self) -> None:
    with (
      self.terminal.cbreak(),
      self.terminal.hidden_cursor(),
      Live(self.pane, refresh_per_second=4, transient=True),
    ):
      try:
        while True:
          ### Process input key ###
          keystroke: Keystroke = self.terminal.inkey(timeout=0.25)
          if keystroke.code == KEY_UP and self.container_index > 0:
            self.container_index -= 1
          elif keystroke.code == KEY_DOWN and self.container_index < len(self.container_names) - 1:
            self.container_index += 1
          elif keystroke in {"Q", "q"}:
            raise StopIteration

          container_rows: str = ""
          if self.container_index > 0:
            container_rows = "\n".join(self.container_names[: self.container_index])
            container_rows += f"\n[reverse]{self.container_names[self.container_index]}[reset]\n"
          else:
            container_rows = f"[reverse]{self.container_names[self.container_index]}[reset]\n"
          if self.container_index < len(self.container_names) - 1:
            container_rows += "\n".join(self.container_names[self.container_index + 1 :])  # noqa: E203
          self.pane["realms"].update(Panel(container_rows, title="realms"))

          container_name: str = self.container_names[self.container_index]
          body_table: Table = Table(expand=True, show_lines=True)
          body_table.add_column(container_name, "dark_sea_green bold")
          if match(r"aesir-(bitcoind)", container_name):
            blockchain_info: BlockchainInfo = TypeAdapter(BlockchainInfo).validate_json(
              self.bitcoind.exec_run(
                """
                bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir getblockchaininfo
                """
              ).output
            )
            mempool_info: MempoolInfo = TypeAdapter(MempoolInfo).validate_json(
              self.bitcoind.exec_run(
                """
                bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir getmempoolinfo
                """
              ).output
            )
            body_table.add_row(
              Text.assemble(
                f"\n{'Blockchain information:'.ljust(20)}\n",
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
          elif match(r"aesir-(electrs)", container_name):
            container: Container = next(
              filter(lambda container: container.name == container_name, self.containers)
            )
            features: JsonrpcResponse[Features] = TypeAdapter(
              JsonrpcResponse[Features]
            ).validate_json(
              container.exec_run(
                [
                  "sh",
                  "-c",
                  """
                echo '{"id": "feat", "jsonrpc": "2.0", "method": "server.features"}' | nc -N localhost 50001
                """,
                ]
              ).output
            )
            body_table.add_row(
              Text.assemble(
                "\n\n\n",
                ("Genesis Hash:".ljust(15), "green bold"),
                features.result.genesis_hash,
                "\n\n".ljust(20),
                ("Hash function:".ljust(16), "cyan bold"),
                f"{features.result.hash_function}".rjust(14),
                "\n".ljust(19),
                ("Pruning?:".ljust(15), "bright_magenta bold"),
                ("true".rjust(15), "green")
                if features.result.pruning
                else ("false".rjust(15), "red"),
                "\n".ljust(19),
                ("Protocol Minimum:".ljust(13), "light_coral bold"),
                f"{features.result.protocol_min}".rjust(13),
                "\n".ljust(19),
                ("Protocol Maximum:".ljust(13), "blue bold"),
                f"{features.result.protocol_max}".rjust(13),
                "\n\n\n",
              )
            )
          elif match(r"aesir-(ord-server)", container_name):
            container: Container = next(
              filter(lambda container: container.name == container_name, self.containers)
            )
            ord_status: OrdStatus = TypeAdapter(OrdStatus).validate_json(
              container.exec_run(
                """
                curl -s -H "Accept: application/json" http://localhost:8080/status
                """
              ).output
            )
            body_table.add_row(
              Text.assemble(
                "\n".ljust(19),
                ("Address index:".ljust(15), "light_coral bold"),
                ("true".rjust(15), "green")
                if ord_status.address_index
                else ("false".rjust(15), "red"),
                "\n".ljust(19),
                ("Blessed:".ljust(15), "rosy_brown bold"),
                f"{ord_status.blessed_inscriptions}".rjust(15),
                "\n".ljust(19),
                ("Cursed:".ljust(15), "hot_pink bold"),
                f"{ord_status.cursed_inscriptions}".rjust(15),
                "\n".ljust(19),
                ("Chain:".ljust(15), "bright_magenta bold"),
                f"{ord_status.chain}".rjust(15),
                "\n".ljust(19),
                ("Inscriptions:".ljust(15), "sandy_brown bold"),
                f"{ord_status.inscriptions}".rjust(15),
                "\n".ljust(19),
                ("Lost sats:".ljust(15), "light_slate_gray bold"),
                f"{ord_status.lost_sats}".rjust(15),
                "\n".ljust(19),
                ("Rune index:".ljust(15), "cyan bold"),
                ("true".rjust(15), "green")
                if ord_status.rune_index
                else ("false".rjust(15), "red"),
                "\n".ljust(19),
                ("Sat Index:".ljust(15), "steel_blue bold"),
                ("true".rjust(15), "green") if ord_status.sat_index else ("false".rjust(15), "red"),
                "\n".ljust(19),
                ("Runes:".ljust(15), "medium_purple bold"),
                f"{ord_status.runes}".rjust(15),
                "\n".ljust(19),
                ("Transaction index:".ljust(13), "dark_sea_green bold"),
                ("true".rjust(13), "green")
                if ord_status.transaction_index
                else ("false".rjust(12), "red"),
                "\n".ljust(19),
                ("Unrecoverably reorged:".ljust(13), "tan bold"),
                ("true".rjust(9), "green")
                if ord_status.unrecoverably_reorged
                else ("false".rjust(8), "red"),
                "\n",
              )
            )
          elif match(r"aesir-(lnd|ping|pong)", container_name):
            container: Container = next(
              filter(lambda container: container.name == container_name, self.containers)
            )
            lnd_info: LNDInfo = TypeAdapter(LNDInfo).validate_json(
              container.exec_run(
                """
                lncli
                  --macaroonpath=/root/.lnd/data/chain/bitcoin/regtest/admin.macaroon
                  --rpcserver=localhost:10001
                  --tlscertpath=/root/.lnd/tls.cert
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
          self.pane["body"].update(body_table)
          self.pane["footer"].update(
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


__all__: tuple[str, ...] = ("Bifrost",)
