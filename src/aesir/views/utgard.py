#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/utgard.py
# VERSION:     0.5.2
# CREATED:     2025-10-03 13:00
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from docker.models.containers import Container
from pydantic import BaseModel, ConfigDict, TypeAdapter
from rich.console import RenderableType
from rich.text import Text

### Local modules ###
from aesir.types import OrdStatus


class Utgard(BaseModel):
  """
  Unpleasantly rough realm and home to giants who mostly disagree with gods.
  """

  model_config = ConfigDict(arbitrary_types_allowed=True)
  container: Container

  @property
  def renderable(self) -> RenderableType:
    ord_status: OrdStatus = TypeAdapter(OrdStatus).validate_json(
      self.container.exec_run(
        """
        curl -s -H "Accept: application/json" http://localhost:8080/status
        """
      ).output
    )
    return Text.assemble(
      "\n".ljust(19),
      ("Address index:".ljust(15), "light_coral bold"),
      ("true".rjust(15), "green") if ord_status.address_index else ("false".rjust(15), "red"),
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
      ("true".rjust(15), "green") if ord_status.rune_index else ("false".rjust(15), "red"),
      "\n".ljust(19),
      ("Sat Index:".ljust(15), "steel_blue bold"),
      ("true".rjust(15), "green") if ord_status.sat_index else ("false".rjust(15), "red"),
      "\n".ljust(19),
      ("Runes:".ljust(15), "medium_purple bold"),
      f"{ord_status.runes}".rjust(15),
      "\n".ljust(19),
      ("Transaction index:".ljust(13), "dark_sea_green bold"),
      ("true".rjust(13), "green") if ord_status.transaction_index else ("false".rjust(12), "red"),
      "\n".ljust(19),
      ("Unrecoverably reorged:".ljust(13), "tan bold"),
      ("true".rjust(9), "green") if ord_status.unrecoverably_reorged else ("false".rjust(8), "red"),
      "\n",
    )


__all__: tuple[str, ...] = ("Utgard",)
