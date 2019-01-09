#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import ocf
import context
import io_utils

lib = ocf.OcfLib.getInstance()
data_obj_list = []

### DATA OPS ###

@CFUNCTYPE(c_void_p, c_uint32)
def data_alloc(pages):
    data = io_utils.Data(pages)
    data_obj_list.append(data)

    return cast(byref(data), c_void_p).value

@CFUNCTYPE(None, c_void_p)
def data_free(data):
    #TODO free data here
    pass

@CFUNCTYPE(c_int, c_void_p)
def data_mlock(data):
    return 0

@CFUNCTYPE(None, c_void_p)
def data_munlock(data):
    pass

@CFUNCTYPE(c_uint32, c_void_p, c_void_p, c_uint32)
def data_rd(dst, src, size):
    return size

@CFUNCTYPE(c_uint32, c_void_p, c_void_p, c_uint32)
def data_wr(dst, src, size):
    return size

@CFUNCTYPE(c_uint32, c_void_p, c_uint32)
def data_zero(dst, size):
    return size

@CFUNCTYPE(c_uint32, c_int, c_uint32)
def data_seek(dst, seek, size):
    return seek

@CFUNCTYPE(c_uint32, c_void_p, c_void_p, c_uint64, c_uint64, c_uint64)
def data_cpy(dst, src, end, start, bytes):
    return bytes

@CFUNCTYPE(None, c_void_p)
def data_secure_erase(dst):
    pass

### QUEUE OPS

@CFUNCTYPE(c_int, c_void_p)
def queue_init(OcfQueue):
    return 0

@CFUNCTYPE(None, c_void_p)
def queue_kick(OcfQueue):
    lib.ocf_queue_run(OcfQueue)

@CFUNCTYPE(None, c_void_p)
def queue_kick_sync(OcfQueue):
    pass

@CFUNCTYPE(None, c_void_p)
def queue_stop(OcfQueue):
    pass

### CLEANER OPS

@CFUNCTYPE(c_int, c_void_p)
def cleaner_init(cleaner):
    return 0

@CFUNCTYPE(None, c_void_p)
def cleaner_stop(cleaner):
    pass

### METADATA OPS

@CFUNCTYPE(c_int, c_void_p)
def metadata_updater_init(OcfMetadataUpdater):
    return 0

@CFUNCTYPE(None, c_void_p)
def metadata_updater_kick(OcfMetadataUpdater):
    pass

@CFUNCTYPE(None, c_void_p)
def metadata_updater_stop(OcfMetadataUpdater):
    pass
