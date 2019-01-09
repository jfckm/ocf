#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
#TODO cleanup this ugly env
# from env import *
import logger
import ocf
from context_ops import *


lib = ocf.OcfLib.getInstance()
#TODO consider changing to some singletons
ctx = None
ops = None
logger_obj = None


class Uuid(Structure):
    _fields_ = [("size", c_size_t),
                ("data", c_void_p)]

#TODO cleanup those...
class OcfQueue(Structure):
    _fields_ = [("cache", c_void_p),
                  ("id", c_uint32),
                  ("io_no", c_int),
                  ("io_list", struct___pthread_internal_list),
                  ("io_list_lock", c_int),
                  ("priv", c_void_p)]

class OcfCleaner(Structure):
    _fields_ = [("priv", c_void_p)]

class OcfMetadataIoSyncher(Structure):
    _fields_ = [("in_progress_head", struct___pthread_internal_list),
                  ("pending_head", struct___pthread_internal_list),
                  ("lock",  c_byte * 40)]

class OcfMetadataUpdater(Structure):
    _fields_ = [("syncher", OcfMetadataIoSyncher),
                  ("priv", c_void_p)]

CTX_OPS_DATA_ALLOC = CFUNCTYPE(c_void_p, c_uint32)
CTX_OPS_DATA_FREE = CFUNCTYPE(None, c_void_p)
CTX_OPS_DATA_MLOCK = CFUNCTYPE(c_int, c_void_p)
CTX_OPS_DATA_MUNLOCK = CFUNCTYPE(c_void_p, c_void_p)
CTX_OPS_DATA_RD = CFUNCTYPE(c_uint32, c_void_p, c_void_p, c_uint32)
CTX_OPS_DATA_WR = CFUNCTYPE(c_uint32, c_void_p, c_void_p, c_uint32)
CTX_OPS_DATA_ZERO = CFUNCTYPE(c_uint32, c_void_p, c_uint32)
CTX_OPS_DATA_SEEK = CFUNCTYPE(c_uint32, c_int, c_uint32)
CTX_OPS_DATA_CPY = CFUNCTYPE(c_void_p, c_void_p, c_uint64, c_uint64, c_uint64, c_uint64)
CTX_OPS_DATA_SECURE_ERASE = CFUNCTYPE(None, c_void_p)

CTX_OPS_QUEUE_INIT = CFUNCTYPE(c_int, OcfQueue)
CTX_OPS_QUEUE_KICK = CFUNCTYPE(None, POINTER(OcfQueue))
CTX_OPS_QUEUE_KICK_SYNC  = CFUNCTYPE(None, OcfQueue)
CTX_OPS_QUEUE_STOP = CFUNCTYPE(None, OcfQueue)

CTX_OPS_CLEANER_INIT = CFUNCTYPE(c_int, OcfCleaner)
CTX_OPS_CLEANER_STOP = CFUNCTYPE(None, OcfCleaner)

CTX_OPS_METADATA_UPDATER_INIT = CFUNCTYPE(c_int, OcfMetadataUpdater)
CTX_OPS_METADATA_UPDATER_KICK = CFUNCTYPE(None, OcfMetadataUpdater)
CTX_OPS_METADATA_UPDATER_STOP = CFUNCTYPE(None, OcfMetadataUpdater)

class CorePool(Structure):
    _fields_ = [("core_pool_head",  struct___pthread_internal_list),
                ("core_pool_count", c_int)]

OCF_RQ_SIZE_MAX = 8

class EnvAllocator(Structure):
    _fields_ = [("name", c_char_p),
                  ("item_size", c_uint32),
                  ("count", c_int)]


class OCfReqAllocator(Structure):
    _fields_ = [("allocator", c_void_p * OCF_RQ_SIZE_MAX),
                  ("size", c_size_t * OCF_RQ_SIZE_MAX)]


class Resources(Structure):
    _fields_ = [("ocf_rq_allocator", c_void_p),
                  ("core_io_allocator", c_void_p)]


OCF_DATA_OBJ_TYPE_MAX = 8

#TODO fixup those
class OcfCtx(Structure):
    _fields_ = [
                ("ctx", c_void_p)
        #              ("ctx_opx", c_void_p),
                # ("logger", c_void_p),
                # ("data_obj_type_array", c_void_p * OCF_DATA_OBJ_TYPE_MAX),
                # ("lock",  c_byte * 40),
                # ("name", c_char_p),
                # ("caches", struct___pthread_internal_list),
                # ("core_pool", CorePool),
                # ("resources", Resources)
    ]


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
    global ctx
    ctx_obj = OcfCtx()
    ctx = pointer(ctx_obj)
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

