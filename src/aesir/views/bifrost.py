#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/bifrost.py
# VERSION:     0.5.4
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
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr
from rich.box import ROUNDED
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

### Local modules ###
from aesir.views.alfheim import Alfheim
from aesir.views.asgard import Asgard
from aesir.views.helheim import Helheim
from aesir.views.midgard import Midgard
from aesir.views.vanaheim import Vanaheim
from aesir.views.utgard import Utgard


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

          body_table: Table = Table(box=ROUNDED, expand=True, show_lines=True)
          container_name: str = self.container_names[self.container_index]
          container: Container = next(
            filter(lambda container: container.name == container_name, self.containers)
          )
          body_table.add_column(container_name, "dark_sea_green bold")
          if match(r"aesir-bitcoind", container_name):
            body_table.add_row(Asgard(container=container).renderable)
          elif match(r"aesir-cashu-mint", container_name):
            body_table.add_row(Vanaheim(container=container).renderable)
          elif match(r"aesir-electrs", container_name):
            body_table.add_row(Alfheim(container=container).renderable)
          elif match(r"aesir-litd", container_name):
            body_table.add_row(Helheim(container=container).renderable)
          elif match(r"aesir-ord-server", container_name):
            body_table.add_row(Utgard(container=container).renderable)
          elif match(r"aesir-(lnd|ping|pong)", container_name):
            body_table.add_row(Midgard(container=container).renderable)
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
