#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/types/image.py
# VERSION: 	   0.4.1
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

ImageAlias = Literal["bitcoind", "cashu-mint", "lnd", "lnd-krub", "ord-server", "postgres", "redis"]
ImageEnum = Literal["optional", "required"]

__all__ = ["ImageAlias", "ImageEnum"]
