#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/configs.py
# VERSION:     0.5.2
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

### Standard packages ###
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
BUILDS: Dict[BuildEnum, Build]
CLUSTERS: Dict[ClusterEnum, Dict[ServiceName, Service]]
NETWORK: str
PERIPHERALS: Dict[ServiceName, Service]

file_path: Path = Path(__file__).resolve()
with open(str(file_path).replace("configs.py", "schemas.yml"), "rb") as stream:
  schema: Optional[Dict[str, Any]] = load(stream, Loader=Loader)
  if schema:
    BUILDS = TypeAdapter(Dict[BuildEnum, Build]).validate_python(schema["builds"])
    CLUSTERS = TypeAdapter(Dict[ClusterEnum, Dict[ServiceName, Service]]).validate_python(
      schema["clusters"]
    )
    NETWORK = schema.get("network", "aesir")
    PERIPHERALS = TypeAdapter(Dict[ServiceName, Service]).validate_python(schema["peripherals"])

__all__: Tuple[str, ...] = ("BUILDS", "CLUSTERS", "NETWORK", "PERIPHERALS")
