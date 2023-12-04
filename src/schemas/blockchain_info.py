#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/schemas/blockchain_info.py
# VERSION: 	   0.2.6
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, StrictInt, StrictStr


class BlockchainInfo(BaseModel):
    blocks: StrictInt
    chain: StrictStr
    size_on_disk: StrictInt
    time: StrictInt


__all__ = ["BlockchainInfo"]
