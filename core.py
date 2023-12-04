#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    core.py
# VERSION: 	   0.2.5
# CREATED: 	   2023-12-01 02:20
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from click import group

### Local modules ###
from src.commands import clean, deploy, flush, mine, nodekeys, ping_pong, setup


@group
def cli() -> None:
    """aesir"""


cli.add_command(clean, "clean")
cli.add_command(deploy, "deploy")
cli.add_command(flush, "flush")
cli.add_command(mine, "mine")
cli.add_command(nodekeys, "nodekeys")
cli.add_command(ping_pong, "ping-pong")
cli.add_command(setup, "setup")


if __name__ == "__main__":
    cli()
