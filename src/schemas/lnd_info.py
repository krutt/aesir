#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/schemas/lnd_info.py
# VERSION: 	   0.2.5
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, StrictBool, StrictInt, StrictStr


class LNDInfo(BaseModel):
    block_height: StrictInt
    identity_pubkey: StrictStr
    num_active_channels: StrictInt
    num_peers: StrictInt
    synced_to_chain: StrictBool


__all__ = ["LNDInfo"]
