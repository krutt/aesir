#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/open_channel.py
# VERSION:     0.5.1
# CREATED:     2023-12-02 20:50
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Tuple

### Third-party packages ###
from pydantic import BaseModel, StrictStr


class OpenChannel(BaseModel):
  funding_txid: StrictStr


__all__: Tuple[str, ...] = ("OpenChannel",)
