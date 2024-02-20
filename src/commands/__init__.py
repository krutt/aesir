#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/__init__.py
# VERSION: 	   0.3.3
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.commands.clean import clean
from src.commands.deploy import deploy
from src.commands.flush import flush
from src.commands.mine import mine
from src.commands.nodekeys import nodekeys
from src.commands.ping_pong import ping_pong
from src.commands.setup import setup

__all__ = ["clean", "deploy", "flush", "mine", "nodekeys", "ping_pong", "setup"]
