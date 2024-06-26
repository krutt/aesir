#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/views/yggdrasil.py
# VERSION:     0.4.4
# CREATED:     2024-06-26 00:14
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from collections import deque
from typing import Deque, Dict, List, Optional, Union

### Third-party packages ###
from rich.box import MINIMAL
from rich.console import ConsoleRenderable, Group, RichCast
from rich.progress import Progress, Task
from rich.table import Table

### Local modules ###
from aesir.types import Build


class Yggdrasil(Progress):
  builds: Dict[str, Build]
  main_task: Task
  rows: Deque[str]
  table: Table = Table(box=MINIMAL, show_lines=False, show_header=False)

  def __init__(self, builds: Dict[str, Build], row_count: int) -> None:
    self.builds = builds
    self.rows = deque(maxlen=row_count)
    super().__init__()

  def __post_init__(self) -> None:
    build_count: int = len(self.builds)
    self.main_task = self.add_task("Build specified images:".ljust(42), total=build_count)

  def get_renderable(self) -> Union[ConsoleRenderable, RichCast, str]:
    return Group(self.table, *self.get_renderables())

  def update_main_task(self, **kwargs) -> None:
    self.update(self.main_task, **kwargs)

  def update_table(self, row: Optional[str] = None) -> None:
    if row is not None:
      self.rows.append(row)
    table: Table = Table(box=MINIMAL, show_lines=False, show_header=False)
    for row_cell in self.rows:
      table.add_row(row_cell[0:92].ljust(92), style="grey50")
    self.table = table


__all__ = ("Yggdrasil",)
