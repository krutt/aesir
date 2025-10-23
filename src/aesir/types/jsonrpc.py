#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/jsonrpc.py
# VERSION:     0.5.4
# CREATED:     2025-10-01 15:50
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, Generic, TypeVar

### Third-party packages ###
from pydantic import BaseModel, Field, StrictInt, StrictStr

T = TypeVar("T")


class JsonrpcError(BaseModel):
  code: StrictInt
  data: None | dict[str, Any] = Field(default=None)
  message: StrictStr


class JsonrpcResponse(BaseModel, Generic[T]):
  id: None | int | str = Field(description="Request identifier")
  error: None | JsonrpcError = Field(default=None, description="Error object when unsuccessful")
  jsonrpc: StrictStr = Field(default="2.0", description="JSON-RPC Version")
  result: None | T = Field(default=None, description="Result object when successful")


__all__: tuple[str, ...] = ("JsonrpcError", "JsonrpcResponse")
