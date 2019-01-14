#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

from ctypes import *
from enum import IntEnum

from .shared import Uuid, OcfError, CacheLineSize, CacheLines
from ..utils import Size, Time
from .core import Core
from .stats.cache import *


class Backfill(Structure):
    _fields_ = [("_max_queue_size", c_uint32), ("_queue_unblock_size", c_uint32)]


class CacheConfig(Structure):
    _fields_ = [
        ("_id", c_uint16),
        ("_name", c_char_p),
        ("_cache_mode", c_uint32),
        ("_eviction_policy", c_uint32),
        ("_cache_line_size", c_uint64),
        ("_metadata_layout", c_uint32),
        ("_metadata_volatile", c_bool),
        ("_backfill", Backfill),
        ("_io_queues", c_uint32),
        ("_locked", c_bool),
        ("_pt_unaligned_io", c_bool),
        ("_use_submit_io_fast", c_bool),
    ]


class CacheDeviceConfig(Structure):
    _fields_ = [
        ("_uuid", Uuid),
        ("_data_obj_type", c_uint8),
        ("_cache_line_size", c_uint64),
        ("_force", c_bool),
        ("_min_free_ram", c_uint64),
        ("_perform_test", c_bool),
        ("_discard_on_start", c_bool),
    ]


class CacheMode(IntEnum):
    WT = (0,)
    WB = (1,)
    WA = (2,)
    PT = (3,)
    WI = 4


class EvictionPolicy(IntEnum):
    LRU = 0


class CleaningPolicy(IntEnum):
    NOP = (0,)
    ALRU = (1,)
    ACP = (2,)
    DEFAULT = ALRU


class MetadataLayout(IntEnum):
    STRIPING = (0,)
    SEQUENTIAL = 1


class Cache:
    DEFAULT_ID = 0
    DEFAULT_MODE = CacheMode.WI
    DEFAULT_EVICTION_POLICY = EvictionPolicy.LRU
    DEFAULT_CACHE_LINE_SIZE = CacheLineSize.DEFAULT
    DEFAULT_METADATA_LAYOUT = MetadataLayout.SEQUENTIAL
    DEFAULT_BACKFILL_QUEUE_SIZE = 65536
    DEFAULT_BACKFILL_UNBLOCK = 60000
    DEFAULT_IO_QUEUES = 1
    DEFAULT_PT_UNALIGNED_IO = False
    DEFAULT_USE_SUBMIT_FAST = False

    def __init__(
        self,
        *,
        cache_id: int,
        name: str,
        cache_mode: CacheMode,
        eviction_policy: EvictionPolicy,
        cache_line_size: int,
        metadata_layout: MetadataLayout,
        metadata_volatile: bool,
        max_queue_size: int,
        queue_unblock_size: int,
        io_queues: int,
        locked: bool,
        pt_unaligned_io: bool,
        use_submit_fast: bool,
        owner
    ):

        self.owner = owner
        self.cache_line_size = cache_line_size
        self.cfg = CacheConfig(
            _id=cache_id,
            _name=name.encode("ascii") if name else None,
            _cache_mode=cache_mode,
            _eviction_policy=eviction_policy,
            _cache_line_size=cache_line_size,
            _metadata_layout=metadata_layout,
            _metadata_volatile=metadata_volatile,
            _backfill=Backfill(
                _max_queue_size=max_queue_size, _queue_unblock_size=queue_unblock_size
            ),
            _io_queues=io_queues,
            _locked=locked,
            _pt_unaligned_io=pt_unaligned_io,
            _use_submit_fast=use_submit_fast,
        )
        self.cache_handle = c_void_p()

        status = self.owner.lib.ocf_mngt_cache_start(
            self.owner.ctx_handle, byref(self.cache_handle), byref(self.cfg)
        )
        if status != 0:
            raise OcfError("Creating cache instance failed", status)

    def attach_device(
        self, device, force=False, perform_test=False, cache_line_size=None
    ):
        self.device_name = device.uuid
        self.dev_cfg = CacheDeviceConfig(
            _uuid=Uuid(
                _data=cast(
                    create_string_buffer(self.device_name.encode("ascii")), c_char_p
                ),
                _size=len(self.device_name) + 1,
            ),
            _data_obj_type=device.type_id,
            _cache_line_size=cache_line_size
            if cache_line_size
            else self.cache_line_size,
            _force=force,
            _min_free_ram=0,
            _perform_test=perform_test,
            _discard_on_start=False,
        )

        status = device.owner.lib.ocf_mngt_cache_attach(
            self.cache_handle, byref(self.dev_cfg)
        )
        if status != 0:
            raise OcfError("Attaching cache device failed", status)

    @classmethod
    def using_device(
        cls,
        device,
        name: str = "",
        cache_id: int = DEFAULT_ID,
        cache_mode: CacheMode = DEFAULT_MODE,
        cache_line_size: int = DEFAULT_CACHE_LINE_SIZE,
    ):

        c = cls(
            cache_id=cache_id,
            name=name,
            cache_mode=cache_mode,
            eviction_policy=cls.DEFAULT_EVICTION_POLICY,
            cache_line_size=cache_line_size,
            metadata_layout=cls.DEFAULT_METADATA_LAYOUT,
            metadata_volatile=False,
            max_queue_size=cls.DEFAULT_BACKFILL_QUEUE_SIZE,
            queue_unblock_size=cls.DEFAULT_BACKFILL_UNBLOCK,
            io_queues=cls.DEFAULT_IO_QUEUES,
            locked=True,
            pt_unaligned_io=cls.DEFAULT_PT_UNALIGNED_IO,
            use_submit_fast=cls.DEFAULT_USE_SUBMIT_FAST,
            owner=device.owner,
        )

        c.attach_device(device, force=True)
        return c

    def add_core(self, core: Core):
        status = self.owner.lib.ocf_mngt_cache_add_core(
            self.cache_handle, byref(core.get_handle()), byref(core.get_cfg())
        )

        if status != 0:
            raise OcfError("Failed adding core", status)

        core.cache = self

    def get_stats(self):
        cache_info = CacheInfo()
        usage = UsageStats()
        req = RequestsStats()
        block = BlocksStats()
        errors = ErrorsStats()

        status = self.owner.lib.ocf_cache_get_info(self.cache_handle, byref(cache_info))
        if status != 0:
            raise OcfError("Failed getting cache info", status)

        status = self.owner.lib.ocf_stats_collect_cache(self.cache_handle,
                byref(usage), byref(req), byref(block), byref(errors))
        if status != 0:
            raise OcfError("Failed getting stats", status)

        line_size = CacheLineSize(cache_info.cache_line_size)
        return {
            "conf": {
                "attached": cache_info.attached,
                "data_obj_type": self.owner.dobj_types[cache_info.data_obj_type],
                "size": CacheLines(cache_info.size, line_size),
                "inactive": {
                    "occupancy": CacheLines(cache_info.inactive.occupancy, line_size),
                    "dirty": CacheLines(cache_info.inactive.dirty, line_size),
                },
                "occupancy": CacheLines(cache_info.occupancy, line_size),
                "dirty": CacheLines(cache_info.dirty, line_size),
                "dirty_initial": CacheLines(cache_info.dirty_initial, line_size),
                "dirty_for": Time.from_s(cache_info.dirty_for),
                "cache_mode": CacheMode(cache_info.cache_mode),
                "fallback_pt": {
                    "error_counter": cache_info.fallback_pt.error_counter,
                    "status": cache_info.fallback_pt.status,
                },
                "state": cache_info.state,
                "eviction_policy": EvictionPolicy(cache_info.eviction_policy),
                "cleaning_policy": CleaningPolicy(cache_info.cleaning_policy),
                "cache_line_size": line_size,
                "flushed": CacheLines(cache_info.flushed, line_size),
                "core_count": cache_info.core_count,
                "metadata_footprint": Size(cache_info.metadata_footprint),
                "metadata_end_offset": Size(cache_info.metadata_end_offset),
            },
            "block" : block,
            "req" : req,
            "usage" : usage,
            "errors" : errors
        }
