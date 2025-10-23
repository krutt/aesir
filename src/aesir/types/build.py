#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/build_enum.py
# VERSION:     0.5.4
# CREATED:     2023-12-06 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

### Third-party packages ###
from pydantic import BaseModel, StrictStr


class Build(BaseModel):
  instructions: list[StrictStr]
  platform: StrictStr = "linux/amd64"


BuildEnum = Literal[
  "aesir-bitcoind",
  "aesir-bitcoind-cat",
  "aesir-cashu-mint",
  "aesir-electrs",
  "aesir-litd",
  "aesir-lnd",
  "aesir-ord-server",
]


__all__: tuple[str, ...] = ("Build", "BuildEnum")
