#
# Copyright(c) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause
#

from ctypes import cast, POINTER

from .cache import Cache
from .io import Io
from .io import IoDir
from .volume_exp_obj import ExpObjVolume
from .volume import Volume


class CacheVolume(ExpObjVolume):
    def __init__(self, cache, open=False, uuid=None):
        super().__init__(cache, uuid)
        self.cache = cache
        self.lib = cache.owner.lib
        if open:
            self.open()

    def open(self):
        return Volume.open(
            self.lib.ocf_cache_get_front_volume(self.cache.handle),
            self
        )

    def md5(self):
        cache_line_size = int(self.cache.get_stats()['conf']['cache_line_size'])
        return self._exp_obj_md5(cache_line_size)
