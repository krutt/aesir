#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/core.py
# VERSION:     0.5.4
# CREATED:     2023-12-01 02:20
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from click import group

### Local modules ###
from aesir.commands import build, clean, deploy, invoice, mine, nodekeys, ping_pong, pull


@group
def cmdline() -> None:
  """aesir"""


cmdline.add_command(build, "build")
cmdline.add_command(clean, "clean")
cmdline.add_command(deploy, "deploy")
cmdline.add_command(invoice, "invoice")
cmdline.add_command(mine, "mine")
cmdline.add_command(nodekeys, "nodekeys")
cmdline.add_command(ping_pong, "ping-pong")
cmdline.add_command(pull, "pull")


if __name__ == "__main__":
  cmdline()
