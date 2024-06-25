#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/views/yggdrasil.py
# VERSION:     0.4.4
# CREATED:     2024-06-25 19:43
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from collections import deque
from typing import Deque, Optional, Union

### Third-party packages ###
from rich.console import ConsoleRenderable, Group, RichCast
from rich.progress import Progress
from rich.table import Table


class Yggdrasil(Progress):
  rows: Deque[str]
  table: Table = Table()

  def __init__(self, row_count: int) -> None:
    self.rows = deque(maxlen=row_count)
    super().__init__()

  def get_renderable(self) -> Union[ConsoleRenderable, RichCast, str]:
    return Group(self.table, *self.get_renderables())

  def update_table(self, row: Optional[str] = None) -> None:
    if row is not None:
      self.rows.append(row)
    table: Table = Table()
    table.add_column("Current progress")
    for row_cell in self.rows:
      table.add_row(row_cell, style="grey50")
    self.table = table


__all__ = ("Yggdrasil",)
