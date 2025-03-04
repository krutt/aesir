#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/open_channel.py
# VERSION:     0.4.9
# CREATED:     2023-12-02 20:50
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, StrictStr


class OpenChannel(BaseModel):
  funding_txid: StrictStr


__all__ = ("OpenChannel",)
