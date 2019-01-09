#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import data_obj as dobj
import ocf
import context

OCF_CORE_NAME_SIZE = 32

#TODO create proper Core class

lib = ocf.OcfLib.getInstance()
core_cfg = None

class UserMetadata(Structure):
    _fields_ = [("data", c_void_p),
                ("size", c_size_t)
               ]

class CoreConfig(Structure):
    _fields_ = [("uuid", context.Uuid),
                #TODO change to enum
                ("data_obj_type", c_uint8),
                ("core_id", c_uint16),
                ("name", c_char_p),
                ("name_size", c_size_t),
                ("cache_id", c_uint16),
                ("try_add", c_bool),
                ("seq_cutoff_threshold", c_uint32),
                ("user_metadata", UserMetadata)
               ]

    def __init__(self):
        name = b'CoreDevConfig'
        self.uuid.data = cast(name, c_void_p)
        self.uuid.size = len(name)
        self.data_obj_type = dobj.data_type["CORE"]
        core_name = b'core1'
        self.name = core_name
        self.name_size = len(core_name)


def add_core(cache, core):
    global core_cfg
    core_cfg = CoreConfig()

    if 0 != lib.ocf_mngt_cache_add_core(cache, byref(core),
                                        byref(core_cfg)):
        print("Add core err!")
        exit(1)

    return 0


