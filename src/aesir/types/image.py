#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/image.py
# VERSION:     0.5.4
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

### Local modules ###
from aesir.types.build import BuildEnum

Image = BuildEnum | Literal["postgres:latest", "redis:latest"]

__all__: tuple[str, ...] = ("Image",)
