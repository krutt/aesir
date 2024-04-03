#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/flush.py
# VERSION: 	   0.4.2
# CREATED: 	   2023-12-01 06:24
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List, Set

### Third-party packages ###
from click import command
from docker import DockerClient, from_env
from docker.errors import DockerException
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from aesir.configs import DEPRECATED


@command
def flush() -> None:
  """Remove images deprecated by workspace."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return
  outputs: List[str] = []
  docker_images: Set[str] = {image.tags[0] for image in client.images.list()}
  for registry_id in track(DEPRECATED, "Remove deprecated images:".ljust(42)):
    if registry_id in docker_images:
      client.images.remove(registry_id)
      outputs.append(f"<Image: '{ registry_id }'> removed.")
  list(map(rich_print, outputs))


__all__ = ["flush"]
