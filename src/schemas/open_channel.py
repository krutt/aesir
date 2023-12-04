#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/schemas/open_channel.py
# VERSION: 	   0.2.6
# CREATED: 	   2023-12-02 20:50
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, StrictStr


class OpenChannel(BaseModel):
    funding_txid: StrictStr


__all__ = ["OpenChannel"]
