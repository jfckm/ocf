#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

from ctypes import *


class _Inactive(Structure):
    _fields_ = [("occupancy", c_uint32), ("dirty", c_uint32)]


class _FallbackPt(Structure):
    _fields_ = [("error_counter", c_int), ("status", c_bool)]


class CacheInfo(Structure):
    _fields_ = [
        ("attached", c_bool),
        ("data_obj_type", c_uint8),
        ("size", c_uint32),
        ("inactive", _Inactive),
        ("occupancy", c_uint32),
        ("dirty", c_uint32),
        ("dirty_initial", c_uint32),
        ("dirty_for", c_uint32),
        ("cache_mode", c_uint32),
        ("fallback_pt", _FallbackPt),
        ("state", c_uint8),
        ("eviction_policy", c_uint32),
        ("cleaning_policy", c_uint32),
        ("cache_line_size", c_uint64),
        ("flushed", c_uint32),
        ("core_count", c_uint32),
        ("metadata_footprint", c_uint64),
        ("metadata_end_offset", c_uint32),
    ]


class _Stat(Structure):
    _fields_ = [("value", c_uint64), ("permil", c_uint64)]


class UsageStats(Structure):
    _fields_ = [
        ("occupancy", _Stat),
        ("free", _Stat),
        ("clean", _Stat),
        ("dirty", _Stat),
    ]


class RequestsStats(Structure):
    _fields_ = [
        ("rd_hits", _Stat),
        ("rd_partial_misses", _Stat),
        ("rd_full_misses", _Stat),
        ("rd_total", _Stat),
        ("wr_hits", _Stat),
        ("wr_partial_misses", _Stat),
        ("wr_full_misses", _Stat),
        ("wr_total", _Stat),
        ("rd_pt", _Stat),
        ("wr_pt", _Stat),
        ("serviced", _Stat),
        ("total", _Stat),
    ]


class BlocksStats(Structure):
    _fields_ = [
        ("core_obj_rd", _Stat),
        ("core_obj_wr", _Stat),
        ("core_obj_total", _Stat),
        ("cache_obj_rd", _Stat),
        ("cache_obj_wr", _Stat),
        ("cache_obj_total", _Stat),
        ("volume_rd", _Stat),
        ("volume_wr", _Stat),
        ("volume_total", _Stat),
    ]


class ErrorsStats(Structure):
    _fields_ = [
        ("core_obj_rd", _Stat),
        ("core_obj_wr", _Stat),
        ("core_obj_total", _Stat),
        ("cache_obj_rd", _Stat),
        ("cache_obj_wr", _Stat),
        ("cache_obj_total", _Stat),
        ("total", _Stat),
    ]
