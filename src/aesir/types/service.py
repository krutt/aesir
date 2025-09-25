#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/service.py
# VERSION:     0.5.2
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List, Literal, Mapping, Tuple

### Third-party packages ###
from pydantic import BaseModel, StrictStr

### Local modules ###
from aesir.types.image import Image


class Service(BaseModel):
  command: Mapping[int, StrictStr] = {}
  env_vars: List[StrictStr] = []
  image: Image
  ports: List[StrictStr]


ServiceName = Literal[
  "aesir-bitcoind",
  "aesir-cashu-mint",
  "aesir-electrs",
  "aesir-lnd",
  "aesir-ord-server",
  "aesir-ping",
  "aesir-pong",
  "aesir-postgres",
  "aesir-redis",
]

__all__: Tuple[str, ...] = ("Service", "ServiceName")
