#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/yggdrasil.py
# VERSION:     0.5.0
# CREATED:     2024-06-26 00:14
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from collections import deque
from json import loads
from math import floor
from re import search
from textwrap import wrap
from typing import Any, Deque, Dict, Generator, Optional, Union

### Third-party packages ###
from rich.box import MINIMAL
from rich.console import ConsoleRenderable, Group, RichCast
from rich.progress import BarColumn, Progress, Task, TaskID
from rich.table import Table


class Yggdrasil(Progress):
  primary_task: Task
  rows: Deque[str]
  table: Table = Table(box=MINIMAL, show_lines=False, show_header=False)

  def __init__(self, row_count: int) -> None:
    self.rows = deque(maxlen=row_count)
    super().__init__()

  def get_renderable(self) -> Union[ConsoleRenderable, RichCast, str]:
    return Group(self.table, *self.get_renderables())

  def get_renderables(self) -> Generator[Table, Any, Any]:
    for task in self.tasks:
      if task.fields.get("progress_type") == "build":
        image_name: str = task.description or "undefined"
        if task.completed < 0:
          self.columns = (f"[red bold]Build unsuccessful for <Image '{image_name}'>.",)
        elif task.completed > 0 and task.completed < 100:
          self.columns = (
            f"Building <[bright_magenta]Image [green]'{image_name}'[reset]>…",
            "".ljust(18),
            BarColumn(),
          )
        else:
          self.columns = (
            f"[blue]Built [reset]<[bright_magenta]Image [green]'{image_name}'[reset]>[blue] successfully.[reset]",
            BarColumn(),
          )
      elif task.fields.get("progress_type") == "primary":
        self.columns = ("Build specified images:".ljust(42), BarColumn())
      yield self.make_tasks_table([task])

  def progress_build(self, chunk: Generator[bytes, None, None], task_id: int) -> None:
    for line in chunk:
      data: Dict[str, Union[Dict[str, str], str]] = loads(line)
      if "stream" in data.keys():
        stream: str = data["stream"].strip()  # type: ignore FIXME
        step = search(r"^STEP (?P<divided>\d+)\/(?P<divisor>\d+):", stream)
        if step is not None:
          divided: int = int(step.group("divided"))
          divisor: int = int(step.group("divisor"))
          self.update(TaskID(task_id), completed=floor(divided / divisor * 100))
        self.update_table(stream)
      elif "errorDetail" in data.keys():
        error: str = data["errorDetail"]["message"].strip()  # type: ignore FIXME
        self.update_table(f"[red]{ error }[reset]")

  def update_table(self, row: Optional[str] = None) -> None:
    if row is not None:
      self.rows.append(row)
    table: Table = Table(box=MINIMAL, show_lines=False, show_header=False)
    map(lambda row: table.add_row("\n".join(wrap(row, width=92)), style="grey50"), self.rows)
    self.table = table


__all__ = ("Yggdrasil",)
