#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/types/blockchain_info.py
# VERSION:     0.4.9
# CREATED:     2024-06-23 14:30
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictFloat


class MempoolInfo(BaseModel):
  full_rbf: StrictBool = Field(
    alias="fullrbf",
    description="True if mempool accepts RBF without replaceability signaling introspection",
  )
  loaded: StrictBool = Field(description="True if mempool is fully loaded")
  max_mempool: StrictInt = Field(
    alias="maxmempool", description="Maxmimum memory usage for the mempool"
  )
  mempool_minimum_fee: StrictFloat = Field(
    alias="mempoolminfee", description="Minimum fee rate in BTC/kvB for transaction to be accepted"
  )
  minimum_relay_transaction_fee: StrictFloat = Field(
    alias="minrelaytxfee", description="Minimum relay fees for transaction"
  )
  total_fee: StrictFloat = Field(description="Total fees for the mempool in BTC")
  txn_count: StrictInt = Field(alias="size", description="Current transaction count")
  txn_bytes: StrictInt = Field(
    alias="bytes", description="Sum of all virtual transaction sizes as defined in BIP-141"
  )
  usage: StrictInt = Field(description="Total memory usage for mempool")
  unbroadcast_count: StrictInt = Field(
    alias="unbroadcastcount",
    description="Number of transactions that have not passed initial broadcast",
  )


__all__ = ("MempoolInfo",)
