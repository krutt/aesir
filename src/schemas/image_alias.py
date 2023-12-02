#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/schemas/image_alias.py
# VERSION: 	   0.2.3
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

ImageAlias = Literal["bitcoind", "lnd", "postgres", "redis"]

__all__ = ["ImageAlias"]
