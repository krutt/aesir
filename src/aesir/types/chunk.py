#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/chunk.py
# VERSION:     0.5.4
# CREATED:     2025-05-05 01:23
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, Field, StrictInt, StrictStr


class ErrorDetail(BaseModel):
  code: StrictInt
  message: StrictStr


class Chunk(BaseModel):
  error: None | StrictStr = None
  error_detail: None | ErrorDetail = Field(alias="errorDetail", default=None)
  stream: None | StrictStr = None


__all__: tuple[str, ...] = ("Chunk", "ErrorDetail")
