#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/blockchain_info.py
# VERSION:     0.5.1
# CREATED:     2024-06-23 14:30
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Tuple

### Third-party packages ###
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictFloat


class MempoolInfo(BaseModel):
  full_rbf: StrictBool = Field(
    alias="fullrbf",
    default=0,
    description="True if mempool accepts RBF without replaceability signaling introspection",
  )
  loaded: StrictBool = Field(default=0, description="True if mempool is fully loaded")
  max_mempool: StrictInt = Field(
    alias="maxmempool", default=0, description="Maxmimum memory usage for the mempool"
  )
  mempool_minimum_fee: StrictFloat = Field(
    alias="mempoolminfee",
    default=0,
    description="Minimum fee rate in BTC/kvB for transaction to be accepted",
  )
  minimum_relay_transaction_fee: StrictFloat = Field(
    alias="minrelaytxfee", default=0, description="Minimum relay fees for transaction"
  )
  total_fee: StrictFloat = Field(default=0, description="Total fees for the mempool in BTC")
  txn_count: StrictInt = Field(alias="size", default=0, description="Current transaction count")
  txn_bytes: StrictInt = Field(
    alias="bytes",
    default=0,
    description="Sum of all virtual transaction sizes as defined in BIP-141",
  )
  usage: StrictInt = Field(default=0, description="Total memory usage for mempool")
  unbroadcast_count: StrictInt = Field(
    alias="unbroadcastcount",
    default=0,
    description="Number of transactions that have not passed initial broadcast",
  )


__all__: Tuple[str, ...] = ("MempoolInfo",)
