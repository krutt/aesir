#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/types/lnd_invoice.py
# VERSION:     0.4.9
# CREATED:     2024-11-15 00:56
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, Field, StrictStr


class LNDInvoice(BaseModel):
  add_index: int
  r_hash: StrictStr
  payment_address: StrictStr = Field(alias="payment_addr")
  payment_request: StrictStr


__all__ = ("LNDInvoice",)
