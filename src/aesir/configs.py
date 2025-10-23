#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/configs.py
# VERSION:     0.5.4
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pathlib import Path
from typing import Any

### Third-party packages ###
from pydantic import TypeAdapter
from yaml import Loader, load

### Local modules ###
from aesir.types import (
  Build,
  BuildEnum,
  ClusterEnum,
  Service,
  ServiceName,
)

### Parse schemas ###
BUILDS: dict[BuildEnum, Build]
CLUSTERS: dict[ClusterEnum, dict[ServiceName, Service]]
NETWORK: str
PERIPHERALS: dict[ServiceName, Service]

file_path: Path = Path(__file__).resolve()
with open(str(file_path).replace("configs.py", "schemas.yml"), "rb") as stream:
  schema: None | dict[str, Any] = load(stream, Loader=Loader)
  if schema:
    BUILDS = TypeAdapter(dict[BuildEnum, Build]).validate_python(schema["builds"])
    CLUSTERS = TypeAdapter(dict[ClusterEnum, dict[ServiceName, Service]]).validate_python(
      schema["clusters"]
    )
    NETWORK = schema.get("network", "aesir")
    PERIPHERALS = TypeAdapter(dict[ServiceName, Service]).validate_python(schema["peripherals"])

__all__: tuple[str, ...] = ("BUILDS", "CLUSTERS", "NETWORK", "PERIPHERALS")
