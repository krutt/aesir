#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/types/peripheral_enum.py
# VERSION: 	   0.3.3
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
