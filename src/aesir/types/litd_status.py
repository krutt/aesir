#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/litd_status.py
# VERSION:     0.5.4
# CREATED:     2025-10-23 19:49
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

### Third-party packages ###
from pydantic import BaseModel, Field, StrictBool, StrictStr


class SubServer(BaseModel):
  custom_status: StrictStr
  disabled: StrictBool
  error: StrictStr
  running: StrictBool


class SubServers(BaseModel):
  accounts: SubServer
  faraday: SubServer
  lit: SubServer
  lnd: SubServer
  loop: SubServer
  pool: SubServer
  taproot_assets: SubServer = Field(alias="taproot-assets")


class LitdStatus(BaseModel):
  state: Literal["SERVER_ACTIVE"]
  sub_servers: SubServers


__all__: tuple[str, ...] = ("LitdStatus", "SubServer", "SubServers")
