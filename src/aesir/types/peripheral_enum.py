#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/aesir/types/peripheral_enum.py
# VERSION: 	   0.3.5
# CREATED: 	   2023-12-03 01:11
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

PeripheralEnum = Literal["cashu-mint", "lnd-krub", "postgres", "redis"]

__all__ = ["PeripheralEnum"]
