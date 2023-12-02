#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/schemas/service.py
# VERSION: 	   0.2.3
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List, Literal

### Third-party packages ###
from pydantic import BaseModel, StrictStr

### Local modules ###
from src.schemas.image_alias import ImageAlias


class Service(BaseModel):
    alias: ImageAlias
    command: List[StrictStr] = []
    env_vars: List[StrictStr] = []
    ports: List[StrictStr]


ServiceName = Literal[
    "tranche-bitcoind",
    "tranche-lnd",
    "tranche-ping",
    "tranche-pong",
    "tranche-postgres",
    "tranche-redis",
]

__all__ = ["Service", "ServiceName"]
