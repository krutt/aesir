#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/types/connection.py
# VERSION:     0.4.9
# CREATED:     2025-03-01 01:23
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

from pydantic import BaseModel, StrictBool, StrictStr


class Connection(BaseModel):
  default: StrictBool
  host: StrictStr
  identity: StrictStr


__all__ = ("Connection",)
