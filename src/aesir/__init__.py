#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/__init__.py
# VERSION:     0.5.1
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Tuple

### Local modules ###
from aesir.commands import build, clean, deploy, invoice, mine, nodekeys, ping_pong, pull

__all__: Tuple[str, ...] = (
  "build",
  "clean",
  "deploy",
  "invoice",
  "mine",
  "nodekeys",
  "ping_pong",
  "pull",
)
__version__: str = "0.5.1"
