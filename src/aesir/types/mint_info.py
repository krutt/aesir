#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/mint_info.py
# VERSION:     0.5.2
# CREATED:     2025-10-05 18:42
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

### Third-party packages ###
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr
from pydantic.json_schema import SkipJsonSchema


class Method(BaseModel):
  commands: SkipJsonSchema[None] | list[StrictStr] = None
  description: SkipJsonSchema[None] | StrictBool = None
  name: StrictStr = Field(alias="method")
  unit: Literal["sat"]


class Nut(BaseModel):
  disabled: SkipJsonSchema[None] | StrictBool = None
  methods: SkipJsonSchema[None] | list[Method] = None
  supported: SkipJsonSchema[None] | StrictBool | list[Method] = None


class MintInfo(BaseModel):
  contact: list[StrictStr]
  name: StrictStr
  pubkey: StrictStr
  version: StrictStr
  time: StrictInt
  nuts: dict[int, Nut]


__all__: tuple[str, ...] = ("Method", "MintInfo", "Nut")
