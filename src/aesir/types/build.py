#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/build_enum.py
# VERSION:     0.5.2
# CREATED:     2023-12-06 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List, Literal, Tuple

### Third-party packages ###
from pydantic import BaseModel, StrictStr


class Build(BaseModel):
  instructions: List[StrictStr]
  platform: StrictStr = "linux/amd64"


BuildEnum = Literal[
  "aesir-bitcoind",
  "aesir-bitcoind-cat",
  "aesir-cashu-mint",
  "aesir-lnd",
  "aesir-lnd-krub",
  "aesir-ord-server",
]


__all__: Tuple[str, ...] = ("Build", "BuildEnum")
