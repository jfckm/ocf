#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import inspect
import data_obj
import ocf
import context
import context_ops
import ocf_io
import io_utils
import test_io_ops as io_ops

lib = ocf.OcfLib.getInstance()

CACHE_SIZE = 100 * 1024 * 1024
CORE_SIZE = 200 * 1024 * 1024

cache_ops = None
cache_d_obj_prop = None
core_ops = None
core_d_obj_prop = None
io_ops_obj = None
cache_storage = None
core_storage = None

@CFUNCTYPE(c_void_p, c_void_p)
def new_io(data_obj):
    lib.ocf_data_obj_new_io.restype = POINTER(ocf_io.OcfIo)
    lib.ocf_data_obj_new_io.argtypes = [c_void_p]
    io = lib.ocf_data_obj_new_io(data_obj)
    if (0 == io):
        print("io alloc failed in new_io")
        exit(1)

    return cast(io, c_void_p).value

def submit_io(io_ptr, storage):
    io = cast(io_ptr, POINTER(ocf_io.OcfIo))
    if (io.contents.dir == ocf_io.dir["WRITE"]):
        dst = byref(storage, io.contents.addr)
        src_ptr = cast(io.contents.ops.contents.get_data(io),
                   POINTER(io_utils.Data))
        src = src_ptr.contents.data
    elif (io.contents.dir == ocf_io.dir["READ"]):
        src = byref(storage, io.contents.addr)
        dst_ptr = cast(io.contents.ops.contents.get_data(io),
                   POINTER(io_utils.Data))
        dst = dst_ptr.contents.data

    memmove(dst, src, io.contents.bytes)

    io.contents.end(io, 0)


@CFUNCTYPE(None, POINTER(ocf_io.OcfIo))
def submit_io_cache(io):
    # print('writing to cache!')
    return submit_io(io, cache_storage)

@CFUNCTYPE(None, POINTER(ocf_io.OcfIo))
def submit_io_core(io):
    # print('writing to core!')
    return submit_io(io, core_storage)

@CFUNCTYPE(None, c_void_p)
def submit_flush(data_obj):
    pass

@CFUNCTYPE(None, c_void_p)
def submit_metadata(data_obj):
    pass

@CFUNCTYPE(None, c_void_p)
def submit_discard(data_obj):
    pass

@CFUNCTYPE(None, c_void_p)
def submit_write_zeroes(data_obj):
    pass


@CFUNCTYPE(c_int, c_void_p)
def open_cache(data_obj):
    global cache_storage
    if (None == cache_storage):
        cache_storage = create_string_buffer(CACHE_SIZE)

    return 0

@CFUNCTYPE(c_int, c_void_p)
def open_core(data_obj):
    global core_storage
    if (None == core_storage):
        core_storage = create_string_buffer(CORE_SIZE)

    return 0

@CFUNCTYPE(None, c_void_p)
def close(data_obj):
    pass


@CFUNCTYPE(c_uint, c_void_p)
def get_max_io_size(data_obj):
    return 128

@CFUNCTYPE(c_uint64, c_void_p)
def core_get_length(data_obj):
    return CORE_SIZE

@CFUNCTYPE(c_uint64, c_void_p)
def cache_get_length(data_obj):
    return CACHE_SIZE

def construct_cache_data_type():
    global cache_ops
    cache_ops = data_obj.DataObjOps()
    cache_ops.new_io = data_obj.OPS_NEW_IO(new_io)
    cache_ops.submit_io = data_obj.OPS_SUBMIT_IO(submit_io_cache)
    cache_ops.submit_flush = data_obj.OPS_SUBMIT_FLUSH(submit_flush)
    cache_ops.submit_metadata = data_obj.OPS_SUBMIT_METADATA(submit_metadata)
    cache_ops.submit_discard = data_obj.OPS_SUBMIT_DISCARD(submit_discard)
    cache_ops.submit_write_zeroes = data_obj.OPS_SUBMIT_WRITE_ZEROES(submit_write_zeroes)

    cache_ops.open = data_obj.OPS_OPEN(open_cache)
    cache_ops.close = data_obj.OPS_CLOSE(close)

    cache_ops.get_max_io_size = data_obj.OPS_GET_MAX_IO_SIZE(get_max_io_size)
    cache_ops.get_length = data_obj.OPS_GET_LENGTH(cache_get_length)

    dobj_prop = data_obj.DataObjProperties()
    dobj_prop.name = b'Cache object props'
    dobj_prop.io_priv_size = sizeof(io_utils.DataObjIo)
    dobj_prop.ops = cache_ops

    global io_ops_obj
    io_ops_obj = ocf_io.OcfIoOps()
    io_ops_obj.set_data = io_ops.io_set_data
    io_ops_obj.get_data = io_ops.io_get_data
    dobj_prop.io_ops = io_ops_obj
    return dobj_prop


def construct_core_data_type():
    global core_ops
    core_ops = data_obj.DataObjOps()

    core_ops.new_io = data_obj.OPS_NEW_IO(new_io)
    core_ops.submit_io = data_obj.OPS_SUBMIT_IO(submit_io_core)
    core_ops.submit_flush = data_obj.OPS_SUBMIT_FLUSH(submit_flush)
    core_ops.submit_metadata = data_obj.OPS_SUBMIT_METADATA(submit_metadata)
    core_ops.submit_discard = data_obj.OPS_SUBMIT_DISCARD(submit_discard)
    core_ops.submit_write_zeroes = data_obj.OPS_SUBMIT_WRITE_ZEROES(submit_write_zeroes)

    core_ops.open = data_obj.OPS_OPEN(open_core)
    core_ops.close = data_obj.OPS_CLOSE(close)

    core_ops.get_max_io_size = data_obj.OPS_GET_MAX_IO_SIZE(get_max_io_size)
    core_ops.get_length = data_obj.OPS_GET_LENGTH(core_get_length)

    dobj_prop = data_obj.DataObjProperties()
    dobj_prop.name = b'Core Object props'
    dobj_prop.io_context_size = sizeof(io_utils.DataObjIo)
    dobj_prop.ops = core_ops

    global io_ops_obj
    io_ops_obj = ocf_io.OcfIoOps()
    io_ops_obj.set_data = io_ops.io_set_data
    io_ops_obj.get_data = io_ops.io_get_data
    dobj_prop.io_ops = io_ops_obj
    return dobj_prop

#TODO make it generic and cleanup functions above
def register_data_obj_types():
    global cache_d_obj_prop
    cache_d_obj_prop = construct_cache_data_type()

    # Register cache data type
    if 0 != lib.ocf_ctx_register_data_obj_type(context.ctx, data_obj.data_type["CACHE"],
                                               byref(cache_d_obj_prop)):
        print ("--- Registering cache data type failed!")
        lib.ocf_ctx_exit(ocf.ctx)
        exit(1)

    global core_d_obj_prop
    core_d_obj_prop = construct_core_data_type()

    # Register core data type
    if 0 != lib.ocf_ctx_register_data_obj_type(context.ctx, data_obj.data_type["CORE"],
                                               byref(core_d_obj_prop)):
        print ("--- Registering core data type failed!")
        lib.ocf_ctx_exit(ocf.ctx)
        exit(1)


### Helpers
def print_storage_buff(storage):
    cnt = 0
    for byte in storage:
        cnt+=1
        if (b'\x00' != byte):
            print ('data: ', byte, 'at offset: ', cnt)

