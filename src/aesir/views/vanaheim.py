#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/vanaheim.py
# VERSION:     0.5.2
# CREATED:     2025-10-05 18:42
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Iterator

### Third-party packages ###
from docker.models.containers import Container
from pydantic import BaseModel, ConfigDict, TypeAdapter
from rich.console import RenderableType
from rich.text import Text

### Local modules ###
from aesir.types import MintInfo


class Vanaheim(BaseModel):
  """
  Lush varied realm sealed off by Odin. Home of the Vanir tribe and deities.
  Flora and fauna abundant with magic, fertility and wisdom.
  """

  model_config = ConfigDict(arbitrary_types_allowed=True)
  container: Container

  @property
  def renderable(self) -> RenderableType:
    mint_info: MintInfo = TypeAdapter(MintInfo).validate_json(
      self.container.exec_run(
        """
        curl -sSL -H "Accept: application/json" http://localhost:3338/v1/info
        """
      ).output
    )
    supported_nuts: list[int] = list(
      map(
        lambda num_nut: num_nut[0],
        filter(lambda num_nut: not num_nut[1].disabled, mint_info.nuts.items()),
      )
    )
    return Text.assemble(
      "\n\n".ljust(20),
      ("Name:".ljust(13), "light_slate_gray bold"),
      f"{mint_info.name}".rjust(17),
      "\n".ljust(19),
      ("Version:".ljust(11), "rosy_brown bold"),
      f"{mint_info.version}".rjust(19),
      "\n\n",
      ("Supported NUTs:\n", "light_coral bold"),
      str(supported_nuts),
      "\n\n",
      ("Pubkey:".ljust(13), "sandy_brown bold"),
      f"{mint_info.pubkey}".rjust(13),
      "\n\n\n",
    )


__all__: tuple[str, ...] = ("Vanaheim",)
