#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/blockchain_info.py
# VERSION:     0.5.4
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, StrictInt, StrictStr


class BlockchainInfo(BaseModel):
  blocks: StrictInt = 0
  chain: StrictStr = ""
  size_on_disk: StrictInt = 0
  time: StrictInt = 0


__all__: tuple[str, ...] = ("BlockchainInfo",)
