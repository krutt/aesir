#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/service.py
# VERSION:     0.5.4
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal, Mapping

### Third-party packages ###
from pydantic import BaseModel, StrictStr

### Local modules ###
from aesir.types.image import Image


class Service(BaseModel):
  command: Mapping[int, StrictStr] = {}
  env_vars: list[StrictStr] = []
  image: Image
  ports: list[StrictStr]


ServiceName = Literal[
  "aesir-bitcoind",
  "aesir-cashu-mint",
  "aesir-electrs",
  "aesir-litd",
  "aesir-lnd",
  "aesir-ord-server",
  "aesir-ping",
  "aesir-pong",
  "aesir-postgres",
  "aesir-redis",
]

__all__: tuple[str, ...] = ("Service", "ServiceName")
