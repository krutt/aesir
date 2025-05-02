#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/lnd_info.py
# VERSION:     0.5.1
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Tuple

### Third-party packages ###
from pydantic import BaseModel, StrictBool, StrictInt, StrictStr


class LNDInfo(BaseModel):
  block_height: StrictInt = 0
  identity_pubkey: StrictStr = ""
  num_active_channels: StrictInt = 0
  num_peers: StrictInt = 0
  synced_to_chain: StrictBool = False


__all__: Tuple[str, ...] = ("LNDInfo",)
