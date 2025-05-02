#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/core.py
# VERSION:     0.5.1
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
def cli() -> None:
  """aesir"""


cli.add_command(build, "build")
cli.add_command(clean, "clean")
cli.add_command(deploy, "deploy")
cli.add_command(invoice, "invoice")
cli.add_command(mine, "mine")
cli.add_command(nodekeys, "nodekeys")
cli.add_command(ping_pong, "ping-pong")
cli.add_command(pull, "pull")


if __name__ == "__main__":
  cli()
