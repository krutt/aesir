#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/ping_pong.py
# VERSION: 	   0.2.1
# CREATED: 	   2023-12-01 06:18
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from click import command


@command
def ping_pong() -> None:
    """For "duo" cluster, create channels between LND nodes."""


__all__ = ["ping_pong"]
