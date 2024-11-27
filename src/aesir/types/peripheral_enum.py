#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/types/peripheral_enum.py
# VERSION:     0.4.9
# CREATED:     2023-12-03 01:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

PeripheralEnum = Literal["cashu-mint", "lnd-krub", "ord-server", "postgres", "redis"]

__all__ = ("PeripheralEnum",)
