#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes

#TODO replace

# if local wordsize is same as target, keep ctypes pointer function.
if ctypes.sizeof(ctypes.c_void_p) == 8:
    POINTER_T = ctypes.POINTER
else:
    # required to access _ctypes
    import _ctypes
    # Emulate a pointer class using the approriate c_int32/c_int64 type
    # The new class should have :
    # ['__module__', 'from_param', '_type_', '__dict__', '__weakref__', '__doc__']
    # but the class should be submitted to a unique instance for each base type
    # to that if A == B, POINTER_T(A) == POINTER_T(B)
    ctypes._pointer_t_type_cache = {}
    def POINTER_T(pointee):
        # a pointer should have the same length as LONG
        fake_ptr_base_type = ctypes.c_uint64 
        # specific case for c_void_p
        if pointee is None: # VOID pointer type. c_void_p.
            pointee = type(None) # ctypes.c_void_p # ctypes.c_ulong
            clsname = 'c_void'
        else:
            clsname = pointee.__name__
        if clsname in ctypes._pointer_t_type_cache:
            return ctypes._pointer_t_type_cache[clsname]
        # make template
        class _T(_ctypes._SimpleCData,):
            _type_ = 'L'
            _subtype_ = pointee
            def _sub_addr_(self):
                return self.value
            def __repr__(self):
                return '%s(%d)'%(clsname, self.value)
            def contents(self):
                raise TypeError('This is not a ctypes pointer.')
            def __init__(self, **args):
                raise TypeError('This is not a ctypes pointer. It is not instanciable.')
        _class = type('LP_%d_%s'%(8, clsname), (_T,),{}) 
        ctypes._pointer_t_type_cache[clsname] = _class
        return _class



uint32_t = ctypes.c_uint32
uint64_t = ctypes.c_uint64
class struct___pthread_internal_list(ctypes.Structure):
    pass

struct___pthread_internal_list._pack_ = True # source:False
struct___pthread_internal_list._fields_ = [
    ('__prev', POINTER_T(struct___pthread_internal_list)),
    ('__next', POINTER_T(struct___pthread_internal_list)),
]

class union_c__UA_pthread_mutex_t(ctypes.Union):
    pass

class struct___pthread_mutex_s(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('__lock', ctypes.c_int32),
    ('__count', ctypes.c_uint32),
    ('__owner', ctypes.c_int32),
    ('__nusers', ctypes.c_uint32),
    ('__kind', ctypes.c_int32),
    ('__spins', ctypes.c_int16),
    ('__elision', ctypes.c_int16),
    ('__list', struct___pthread_internal_list),
     ]

union_c__UA_pthread_mutex_t._pack_ = True # source:False
union_c__UA_pthread_mutex_t._fields_ = [
    ('__data', struct___pthread_mutex_s),
    ('__size', ctypes.c_char * 40),
    ('__align', ctypes.c_int64),
    # ('PADDING_0', ctypes.c_ubyte * 32),
]

class union_c__UA_pthread_rwlock_t(ctypes.Union):
    pass

class struct_c__UA_pthread_rwlock_t_0(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('__lock', ctypes.c_int32),
    ('__nr_readers', ctypes.c_uint32),
    ('__readers_wakeup', ctypes.c_uint32),
    ('__writer_wakeup', ctypes.c_uint32),
    ('__nr_readers_queued', ctypes.c_uint32),
    ('__nr_writers_queued', ctypes.c_uint32),
    ('__writer', ctypes.c_int32),
    ('__shared', ctypes.c_int32),
    ('__rwelision', ctypes.c_byte),
    ('__pad1', ctypes.c_ubyte * 7),
    ('__pad2', ctypes.c_uint64),
    ('__flags', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

union_c__UA_pthread_rwlock_t._pack_ = True # source:False
union_c__UA_pthread_rwlock_t._fields_ = [
    ('__data', struct_c__UA_pthread_rwlock_t_0),
    ('__size', ctypes.c_char * 56),
    ('__align', ctypes.c_int64),
    ('PADDING_0', ctypes.c_ubyte * 48),
]

class union_c__UA_sem_t(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('__size', ctypes.c_char * 32),
    ('__align', ctypes.c_int64),
    ('PADDING_0', ctypes.c_ubyte * 24),
     ]

u8 = ctypes.c_ubyte
u16 = ctypes.c_uint16
u32 = ctypes.c_uint32
u64 = ctypes.c_uint64
sector_t = ctypes.c_uint64
class struct__env_allocator(ctypes.Structure):
    pass

env_allocator = struct__env_allocator
class struct_c__SA_env_mutex(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('m', union_c__UA_pthread_mutex_t),
     ]

env_mutex = struct_c__SA_env_mutex
env_rmutex = struct_c__SA_env_mutex
class struct_c__SA_env_rwsem(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('lock', union_c__UA_pthread_rwlock_t),
     ]

env_rwsem = struct_c__SA_env_rwsem
class struct_completion(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('sem', union_c__UA_sem_t),
     ]

env_completion = struct_completion
class struct_c__SA_env_atomic(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('counter', ctypes.c_int32),
     ]

env_atomic = struct_c__SA_env_atomic
class struct_c__SA_env_atomic64(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('counter', ctypes.c_int64),
     ]

env_atomic64 = struct_c__SA_env_atomic64
class struct_c__SA_env_spinlock(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('lock', ctypes.c_int32),
     ]

env_spinlock = struct_c__SA_env_spinlock
class struct_c__SA_env_rwlock(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('lock', union_c__UA_pthread_rwlock_t),
     ]

env_rwlock = struct_c__SA_env_rwlock
class struct_c__SA_env_waitqueue(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('sem', union_c__UA_sem_t),
     ]

env_waitqueue = struct_c__SA_env_waitqueue
class struct_env_timeval(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('sec', ctypes.c_uint64),
    ('usec', ctypes.c_uint64),
     ]

__all__ = \
    ['env_allocator', 'env_atomic', 'env_atomic64', 'env_completion',
    'env_mutex', 'env_rmutex', 'env_rwlock', 'env_rwsem',
    'env_spinlock', 'env_waitqueue', 'sector_t',
    'struct___pthread_internal_list', 'struct___pthread_mutex_s',
    'struct__env_allocator', 'struct_c__SA_env_atomic',
    'struct_c__SA_env_atomic64', 'struct_c__SA_env_mutex',
    'struct_c__SA_env_rwlock', 'struct_c__SA_env_rwsem',
    'struct_c__SA_env_spinlock', 'struct_c__SA_env_waitqueue',
    'struct_c__UA_pthread_rwlock_t_0', 'struct_completion',
    'struct_env_timeval', 'u16', 'u32', 'u64', 'u8', 'uint32_t',
    'uint64_t', 'union_c__UA_pthread_mutex_t',
    'union_c__UA_pthread_rwlock_t', 'union_c__UA_sem_t']
