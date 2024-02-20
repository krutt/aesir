#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/types/service.py
# VERSION: 	   0.3.3
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
from src.types.image import ImageAlias


class Service(BaseModel):
  alias: ImageAlias
  command: List[StrictStr] = []
  env_vars: List[StrictStr] = []
  ports: List[StrictStr]


ServiceName = Literal[
  "aesir-bitcoind",
  "aesir-cashu-mint",
  "aesir-lnd",
  "aesir-lnd-krub",
  "aesir-ping",
  "aesir-pong",
  "aesir-postgres",
  "aesir-redis",
]

__all__ = ["Service", "ServiceName"]
