#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/types/service.py
# VERSION:     0.4.9
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List, Literal

### Third-party packages ###
from pydantic import BaseModel, StrictStr

### Local modules ###
from aesir.types.image import ImageAlias


class Service(BaseModel):
  alias: ImageAlias
  command: List[StrictStr] = []
  env_vars: List[StrictStr] = []
  ports: List[StrictStr]


ServiceName = Literal[
  "aesir-bitcoind",
  "aesir-bitcoind-cat",
  "aesir-cashu-mint",
  "aesir-lnd",
  "aesir-lnd-krub",
  "aesir-ord-server",
  "aesir-ping",
  "aesir-pong",
  "aesir-postgres",
  "aesir-redis",
]

__all__ = ("Service", "ServiceName")
