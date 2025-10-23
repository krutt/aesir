#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/electrs_features.py
# VERSION:     0.5.4
# CREATED:     2025-10-01 15:50
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

### Third-party packages ###
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr


class ElectrsFeatures(BaseModel):
  genesis_hash: StrictStr
  hash_function: StrictStr = Field(default="sha256")
  hosts: dict[Literal["tcp_port"], StrictInt]
  protocol_max: StrictStr = Field(default="1.4")
  protocol_min: StrictStr = Field(default="1.4")
  pruning: None | StrictBool = Field(default=None)
  server_version: StrictStr = Field(default="electrs/0.10.10")


__all__: tuple[str, ...] = ("ElectrsFeatures",)
