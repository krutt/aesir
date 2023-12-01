#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/schemas/node_info.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, StrictStr


class NodeInfo(BaseModel):
    identity_pubkey: StrictStr


__all__ = ["NodeInfo"]
