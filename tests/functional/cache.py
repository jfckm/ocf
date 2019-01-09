#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import context
import ocf
import data_obj as dobj

lib = ocf.OcfLib.getInstance()
cache_obj = None

cache_mode = {"wt" : 0,
              "wb" : 1,
              "wa" : 2,
              "pt" : 3,
              "wi" : 4}

class List(Structure):
    _fields_ = [("next", c_void_p),
                ("prev", c_void_p)]


#TODO fix fields
class Cache(Structure):
    _fields_ = [("owner", context.OcfCtx),
                ("stuff", c_uint8 * 591960)]
               #  ("list", List),
                # ("valid_ocf_cache_device_t", c_uint8),
                # ("cache_state", c_ulong),
                # ("ref_count", c_int),
                # ("conf_met", c_void_p),
                # ("device" , c_void_p)]

class Backfill(Structure):
    _fields_ = [("max_queue_size", c_uint32),
                ("queue_unblock_size", c_uint32)]

class CacheConfig(Structure):
    _fields_ = [("id", c_uint16),
                ("name", c_char_p),
                ("name_size", c_size_t),
                ("cache_mode", c_uint32),
                ("eviction_policy", c_uint32),
                ("cache_line_size", c_uint64),
                ("metadata_layout", c_uint32),
                ("metadata_volatile", c_bool),
                ("backfill", Backfill),
                ("io_queues", c_uint32),
                ("locked", c_bool),
                ("pt_unaligned_io", c_bool),
                ("use_submit_io_fast", c_bool)
               ]

    def __init__(self, cache_line_size=4096, cache_mode=cache_mode["wt"],
                 io_queues=1):
        self.cache_line_size = cache_line_size
        self.cache_mode = cache_mode
        self.io_queues = io_queues


class CacheDeviceConfig(Structure):
    _fields_ = [("uuid", context.Uuid),
                #TODO change to enum
                ("data_obj_type", c_uint8),
                ("cache_line_size", c_uint64),
                ("force", c_bool),
                ("min_free_ram", c_uint64),
                ("perform_test", c_bool),
                ("discard_on_start", c_bool)
               ]

    def __init__(self, min_free_ram = 1024):
        name = b'CacheDevConfig'
        self.uuid.data = cast(name, c_void_p)
        self.uuid.size = len(name)
        self.data_obj_type = dobj.data_type["CACHE"]
        self.min_free_ram = min_free_ram


def start_cache(mode=cache_mode["wt"]):
    global cache_obj
    cache_obj = Cache()
    cache_ptr = pointer(cache_obj)

    cache_cfg = CacheConfig(cache_mode=mode)

    if 0 != lib.ocf_mngt_cache_start(context.ctx, byref(cache_ptr), byref(cache_cfg)):
        print ("---  Creating cache_obj type failed!")
        lib.ocf_ctx_exit(context.ctx)
        exit(1)

    cache_dev_cfg = CacheDeviceConfig()

    if 0 != lib.ocf_mngt_cache_attach(cache_ptr, byref(cache_dev_cfg)):
        print ("---  Attaching cache dev failed!")
        lib.ocf_ctx_exit(context.ctx)
        exit(1)

    return cache_ptr

