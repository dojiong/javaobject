from .build import *
from . import javabuiltins
from .javacls import JavaClass
from .ser import Serializable
from .field import *
from .array import Array


def build_object(obj, get_blockdata):
    cls = JavaClass.resolve(obj.desc.name)
    if cls is None:
        raise TypeError('invalid class : %s' % obj.desc.name)
    newobj = cls.__new__(cls)
    for k, field in cls.__fields__.items():
        setattr(newobj, k, obj.fields[field.name])
    if hasattr(newobj, '__build__') and callable(newobj.__build__):
        newobj.__build__(obj)

    if isinstance(newobj, Serializable):
        blockdata = get_blockdata()
        newobj.decode(blockdata)

    return newobj.__topy__()


def build_array(ary):
    field = resolve_field(consts.TP_ARRAY, '', ary.desc.name)
    if field is None:
        raise TypeError('invalid array : %s' % obj.desc.name)
    return ary.data


def build_eunm(enum):
    cls = JavaClass.resolve(obj.desc.name)
    if cls is None:
        raise TypeError('invalid enum : %s' % obj.desc.name)
    return cls(enum.value)
