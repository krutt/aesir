#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/litd_info.py
# VERSION:     0.5.4
# CREATED:     2025-10-23 19:49
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, StrictStr


class LitdInfo(BaseModel):
  commit_hash: StrictStr
  version: StrictStr


__all__: tuple[str, ...] = ("LitdInfo",)
