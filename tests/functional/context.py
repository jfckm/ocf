#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import logger
import ocf
from context_ops import *


lib = ocf.OcfLib.getInstance()
ctx = c_void_p()
ops = None
logger_obj = None


CTX_OPS_DATA_ALLOC = CFUNCTYPE(c_void_p, c_uint32)
CTX_OPS_DATA_FREE = CFUNCTYPE(None, c_void_p)
CTX_OPS_DATA_MLOCK = CFUNCTYPE(c_int, c_void_p)
CTX_OPS_DATA_MUNLOCK = CFUNCTYPE(None, c_void_p)
CTX_OPS_DATA_RD = CFUNCTYPE(c_uint32, c_void_p, c_void_p, c_uint32)
CTX_OPS_DATA_WR = CFUNCTYPE(c_uint32, c_void_p, c_void_p, c_uint32)
CTX_OPS_DATA_ZERO = CFUNCTYPE(c_uint32, c_void_p, c_uint32)
CTX_OPS_DATA_SEEK = CFUNCTYPE(c_uint32, c_int, c_uint32)
CTX_OPS_DATA_CPY = CFUNCTYPE(c_void_p, c_void_p, c_uint64, c_uint64, c_uint64, c_uint64)
CTX_OPS_DATA_SECURE_ERASE = CFUNCTYPE(None, c_void_p)

CTX_OPS_QUEUE_INIT = CFUNCTYPE(c_int, c_void_p)
CTX_OPS_QUEUE_KICK = CFUNCTYPE(None, POINTER(c_void_p))
CTX_OPS_QUEUE_KICK_SYNC  = CFUNCTYPE(None, c_void_p)
CTX_OPS_QUEUE_STOP = CFUNCTYPE(None, c_void_p)

CTX_OPS_CLEANER_INIT = CFUNCTYPE(c_int, c_void_p)
CTX_OPS_CLEANER_STOP = CFUNCTYPE(None, c_void_p)

CTX_OPS_METADATA_UPDATER_INIT = CFUNCTYPE(c_int, c_void_p)
CTX_OPS_METADATA_UPDATER_KICK = CFUNCTYPE(None, c_void_p)
CTX_OPS_METADATA_UPDATER_STOP = CFUNCTYPE(None, c_void_p)

class Uuid(Structure):
    _fields_ = [("size", c_size_t),
                ("data", c_void_p)]


class OcfCtxOps(Structure):
    _fields_ = [("name", c_char_p),

               ("data_alloc", CTX_OPS_DATA_ALLOC),
               ("data_free", CTX_OPS_DATA_FREE),
               ("data_mlock", CTX_OPS_DATA_MLOCK),
               ("data_munlock", CTX_OPS_DATA_MUNLOCK),
               ("data_rd", CTX_OPS_DATA_RD),
               ("data_wr", CTX_OPS_DATA_WR),
               ("data_zero", CTX_OPS_DATA_ZERO),
               ("data_seek", CTX_OPS_DATA_SEEK),
               ("data_cpy", CTX_OPS_DATA_CPY),
               ("data_secure_erase", CTX_OPS_DATA_SECURE_ERASE),

               ("queue_init", CTX_OPS_QUEUE_INIT),
               ("queue_kick", CTX_OPS_QUEUE_KICK),
               ("queue_kick_async", CTX_OPS_QUEUE_KICK_SYNC),
               ("queue_stop", CTX_OPS_QUEUE_STOP),

               ("cleaner_init", CTX_OPS_CLEANER_INIT),
               ("cleaner_stop", CTX_OPS_CLEANER_STOP),

               ("metadata_updater_init", CTX_OPS_METADATA_UPDATER_INIT),
               ("metadata_updater_kick", CTX_OPS_METADATA_UPDATER_KICK),
               ("metadata_updater_stop", CTX_OPS_METADATA_UPDATER_STOP)
               ]


def CreateOps():
    ops = OcfCtxOps()

    ops.data_alloc =  CTX_OPS_DATA_ALLOC(data_alloc)
    ops.data_free = CTX_OPS_DATA_FREE(data_free)
    ops.data_mlock = CTX_OPS_DATA_MLOCK(data_mlock)
    ops.data_munlock = CTX_OPS_DATA_MUNLOCK(data_munlock)
    ops.data_rd= CTX_OPS_DATA_RD(data_rd)
    ops.data_wr = CTX_OPS_DATA_WR(data_wr)
    ops.data_zero = CTX_OPS_DATA_ZERO(data_zero)
    ops.data_seek = CTX_OPS_DATA_SEEK(data_seek)
    ops.data_cpy = CTX_OPS_DATA_CPY(data_cpy)
    ops.data_secure_erase = CTX_OPS_DATA_SECURE_ERASE(data_secure_erase)

    ops.queue_init = CTX_OPS_QUEUE_INIT(queue_init)
    ops.queue_kick = CTX_OPS_QUEUE_KICK(queue_kick)
    ops.queue_kick_sync = CTX_OPS_QUEUE_KICK_SYNC(queue_kick_sync)
    ops.queue_stop = CTX_OPS_QUEUE_STOP(queue_stop)

    ops.cleaner_init = CTX_OPS_CLEANER_INIT(cleaner_init)
    ops.cleaner_stop = CTX_OPS_CLEANER_STOP(cleaner_stop)

    ops.metadata_updater_init = CTX_OPS_METADATA_UPDATER_INIT(metadata_updater_init)
    ops.metadata_updater_kick = CTX_OPS_METADATA_UPDATER_KICK(metadata_updater_kick)
    ops.metadata_updater_stop = CTX_OPS_METADATA_UPDATER_STOP(metadata_updater_stop)

    return ops

def CreateCtx():
    ocf_ctx = OcfCtx()
    ops = CreateOps()
    ctx = Context(ocf_ctx, ops)
    ctx.ops.name = b'OCF Test Framework'

    return ctx

def InitCtx():
    lib = ocf.OcfLib.getInstance()
    global ops
    ops = CreateOps()
    ops.name = b'OCF Test Framework'

    # Init ocf context
    if 0 != lib.ocf_ctx_init((pointer(ctx)),  byref(ops)):
        print ("--- Ctx init failed!")
        exit(1)

    global logger_obj
    logger_obj = logger.CreateLogger()
    # Set logger
    if 0 != lib.ocf_ctx_set_logger(ctx, pointer(logger_obj)):
        print("--- Setting logger failed!")
        lib.ocf_ctx.exit(context.ctx)
        exit(1)

