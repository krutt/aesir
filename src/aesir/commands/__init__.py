#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/__init__.py
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
from aesir.commands.build import build
from aesir.commands.clean import clean
from aesir.commands.deploy import deploy
from aesir.commands.invoice import invoice
from aesir.commands.mine import mine
from aesir.commands.nodekeys import nodekeys
from aesir.commands.ping_pong import ping_pong
from aesir.commands.pull import pull

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
