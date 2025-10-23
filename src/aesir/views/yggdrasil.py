#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/yggdrasil.py
# VERSION:     0.5.4
# CREATED:     2024-06-26 00:14
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from collections import deque
from math import floor
from re import search
from textwrap import wrap
from typing import Deque, Generator

### Third-party packages ###
from rich.box import MINIMAL
from rich.console import ConsoleRenderable, Group, RichCast
from rich.progress import BarColumn, Progress, Task, TaskID
from rich.table import Table


### Local modules ###
from aesir.exceptions import BuildUnsuccessful
from aesir.types import Chunk


class Yggdrasil(Progress):
  primary_task: Task
  rows: Deque[str]
  table: Table = Table(box=MINIMAL, show_lines=False, show_header=False)

  def __init__(self, row_count: int) -> None:
    self.rows = deque(maxlen=row_count)
    super().__init__()

  def get_renderable(self) -> ConsoleRenderable | RichCast | str:
    return Group(self.table, *self.get_renderables())

  def get_renderables(self) -> Generator[Table, None, None]:
    for task in self.tasks:
      if task.fields.get("progress_type") == "build":
        image_name: str = task.description or "undefined"
        if task.completed < 0:
          self.columns = (
            f"[red bold]Build unsuccessful for <Image '{image_name}'>.",
            "".ljust(9),
            BarColumn(),
          )
        elif task.completed == 0:
          self.columns = (
            f"Preparing to build <[bright_magenta]Image [green]'{image_name}'[reset]>…",
            "".ljust(9),
            BarColumn(),
          )
        elif task.completed > 0 and task.completed < 100:
          self.columns = (
            f"Building <[bright_magenta]Image [green]'{image_name}'[reset]>…",
            "".ljust(9),
            BarColumn(),
          )
        else:
          self.columns = (
            f"[blue]Built [reset]<[bright_magenta]Image [green]'{ image_name }'[reset]>"
            "[blue] successfully.[reset]",
            BarColumn(),
          )
      elif task.fields.get("progress_type") == "primary":
        self.columns = ("Build specified images:".ljust(42), BarColumn())
      yield self.make_tasks_table([task])

  def progress_build(self, chunks: Generator[dict[str, str], None, None], task_id: TaskID) -> None:
    """
    :raises BuildUnsuccessful:
    :raises pydantic.ValidationError:
    """
    for dictionary in chunks:
      chunk: Chunk = Chunk.model_validate(dictionary)
      if chunk.stream is not None:
        step = search(r"^Step (?P<divided>\d+)\/(?P<divisor>\d+) :", chunk.stream)
        if step is not None:
          divided: int = int(step.group("divided"))
          divisor: int = int(step.group("divisor"))
          self.update(task_id, completed=floor(divided / divisor * 100))
        self.update_table(chunk.stream)
      elif chunk.error is not None:
        self.update_table(f"[red]{chunk.error}[reset]")
        if chunk.error_detail is not None:
          raise BuildUnsuccessful(code=chunk.error_detail.code, message=chunk.error_detail.message)
        else:
          raise BuildUnsuccessful(code=255, message=chunk.error)

  def update_table(self, row: None | str = None) -> None:
    if row is not None:
      self.rows.append(row)
    table: Table = Table(box=MINIMAL, show_lines=False, show_header=False)
    list(map(lambda row: table.add_row("\n".join(wrap(row, width=92)), style="grey50"), self.rows))
    self.table = table


__all__: tuple[str, ...] = ("Yggdrasil",)
