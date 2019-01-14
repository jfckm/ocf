#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

from ctypes import *
from enum import IntEnum
from .logger import LoggerOps
from .data import DataOps
from .queue import QueueOps
from .cleaner import CleanerOps
from .metadata_updater import MetadataUpdaterOps


class OcfCtxOps(Structure):
    _fields_ = [
        ("data", DataOps),
        ("queue", QueueOps),
        ("cleaner", CleanerOps),
        ("metadata_updater", MetadataUpdaterOps),
        ("logger", LoggerOps),
    ]


class OcfCtxCfg(Structure):
    _fields_ = [("name", c_char_p), ("ops", OcfCtxOps), ("logger_priv", c_void_p)]


class OcfCtx:
    def __init__(self, lib, name, logger, data, mu, queue, cleaner):
        self.logger = logger
        self.data = data
        self.mu = mu
        self.queue = queue
        self.cleaner = cleaner
        self.ctx_handle = c_void_p()
        self.lib = lib
        self.dobj_types_count = 1
        self.dobj_types = {}

        self.cfg = OcfCtxCfg(
            name=name,
            ops=OcfCtxOps(
                data=self.data.get_ops(),
                queue=self.queue.get_ops(),
                cleaner=self.cleaner.get_ops(),
                metadata_updater=self.mu.get_ops(),
                logger=logger.get_ops(),
            ),
            logger_priv=cast(logger, c_void_p),
        )

        result = self.lib.ocf_ctx_init(byref(self.ctx_handle), byref(self.cfg))
        if result != 0:
            raise OcfError("Context initialization failed", result)

    def register_data_object_type(self, dobj_type):
        self.dobj_types[self.dobj_types_count] = dobj_type.get_props()
        dobj_type.type_id = self.dobj_types_count
        dobj_type.owner = self

        result = self.lib.ocf_ctx_register_data_obj_type(
            self.ctx_handle,
            self.dobj_types_count,
            byref(self.dobj_types[self.dobj_types_count]),
        )
        if result != 0:
            raise OcfError("Data object registration failed", result)

        self.dobj_types_count += 1

    def __del__(self):
        self.lib.ocf_ctx_exit(self.ctx_handle)
