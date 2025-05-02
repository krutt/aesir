#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/build_enum.py
# VERSION:     0.5.1
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


BuildEnum = Literal["bitcoind", "bitcoind-cat", "cashu-mint", "lnd", "lnd-krub", "ord-server"]


__all__: Tuple[str, ...] = ("Build", "BuildEnum")
