#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/configs.py
# VERSION: 	   0.2.4
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pathlib import Path
from typing import Any, Dict, List, Optional

### Standard packages ###
from pydantic import TypeAdapter
from yaml import Loader, load

### Local modules ###
from src.schemas import ClusterEnum, ImageAlias, Service, ServiceName

CLUSTERS: Dict[ClusterEnum, Dict[ServiceName, Service]]
DEPRECATED: List[str]
IMAGES: Dict[ImageAlias, str]
NETWORK: str

file_path: Path = Path(__file__).resolve()
with open(str(file_path).replace("configs.py", "constants.yaml"), "rb") as stream:
    constants: Optional[Dict[str, Any]] = load(stream, Loader=Loader)
    if constants:
        CLUSTERS = TypeAdapter(Dict[ClusterEnum, Dict[ServiceName, Service]]).validate_python(
            constants["clusters"]
        )
        DEPRECATED = constants.get("deprecated", [])
        IMAGES = TypeAdapter(Dict[ImageAlias, str]).validate_python(constants["images"])
        NETWORK = constants.get("network", "tranche")

__all__ = ["CLUSTERS", "DEPRECATED", "IMAGES", "NETWORK"]
