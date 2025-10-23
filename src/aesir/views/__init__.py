#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/__init__.py
# VERSION:     0.5.4
# CREATED:     2024-06-25 19:43
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Local modules ###
from aesir.views.alfheim import Alfheim
from aesir.views.asgard import Asgard
from aesir.views.bifrost import Bifrost
from aesir.views.utgard import Utgard
from aesir.views.vanaheim import Vanaheim
from aesir.views.yggdrasil import Yggdrasil

__all__: tuple[str, ...] = ("Alfheim", "Asgard", "Bifrost", "Utgard", "Vanaheim", "Yggdrasil")
