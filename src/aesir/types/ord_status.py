#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/ord_status.py
# VERSION:     0.5.4
# CREATED:     2025-10-02 14:09
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

### Third-party packages ###
from pydantic import BaseModel, StrictBool, StrictInt, StrictStr


class OrdStatus(BaseModel):
  address_index: StrictBool
  blessed_inscriptions: StrictInt
  chain: Literal["mainnet", "regtest", "signet", "testnet"]
  cursed_inscriptions: StrictInt
  height: StrictInt
  initial_sync_time: dict[Literal["secs", "nanos"], StrictInt]
  inscriptions: StrictInt
  lost_sats: StrictInt
  minimum_rune_for_next_block: StrictStr
  rune_index: StrictBool
  runes: StrictInt
  sat_index: StrictBool
  started: StrictStr
  transaction_index: StrictBool
  unrecoverably_reorged: StrictBool
  uptime: dict[Literal["secs", "nanos"], StrictInt]


__all__: tuple[str, ...] = ("OrdStatus",)
