#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/schemas/image.py
# VERSION: 	   0.2.6
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

ImageAlias = Literal["bitcoind", "lnd", "postgres", "redis"]
ImageEnum = Literal["optional", "required"]

__all__ = ["ImageAlias", "ImageEnum"]
