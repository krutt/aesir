#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/types/build_enum.py
# VERSION: 	   0.4.1
# CREATED: 	   2023-12-06 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List, Literal

from pydantic import BaseModel, StrictStr


class Build(BaseModel):
  instructions: List[StrictStr]
  platform: StrictStr = "linux/amd64"


BuildEnum = Literal["cashu-mint", "lnd-krub", "ord-server", "tesla-ball"]


__all__ = ["Build", "BuildEnum"]
