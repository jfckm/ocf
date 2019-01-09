#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import inspect
import ocf
import io_utils

lib = ocf.OcfLib.getInstance()
data_obj_list = []

### DATA OPS ###

def data_alloc(pages):
    data = io_utils.Data(pages)
    data_obj_list.append(data)

    # data.data = cast(create_string_buffer(4096 * pages), c_void_p)
    # ptr_cast = cast(byref(data), c_void_p)
    # return ptr_cast.value
    return cast(byref(data), c_void_p).value

def data_free(data):
    data_ptr = cast(data, POINTER(io_utils.Data))

    #TODO add proper cleanup
#     for x in data_obj_list:
        # if x.data == data_ptr.contents.data:
            # del x

@CFUNCTYPE(c_int, c_void_p)
def data_mlock(data):
    return 0

def data_munlock(data):
    pass

#TODO add actual read/write
def data_rd(dst, src, size):
    return size

def data_wr(dst, src, size):
    return size

def data_zero(dst, size):
    return size

def data_seek(dst, seek, size):
    return seek

@CFUNCTYPE(c_uint32, c_void_p, c_void_p, c_uint64, c_uint64, c_uint64)
def data_cpy(dst, src, end, start, bytes):
    return bytes

def data_secure_erase(dst):
    pass

### QUEUE OPS

def queue_init(OcfQueue):
    return 0

def queue_kick(OcfQueue):
    lib.ocf_queue_run(OcfQueue)

def queue_kick_sync(OcfQueue):
    pass

def queue_stop(OcfQueue):
    pass

### CLEANER OPS

def cleaner_init(cleaner):
    return 0

def cleaner_stop(cleaner):
    pass

### METADATA OPS

def metadata_updater_init(OcfMetadataUpdater):
    return 0

def metadata_updater_kick(OcfMetadataUpdater):
    pass

def metadata_updater_stop(OcfMetadataUpdater):
    pass
