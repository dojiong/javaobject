from .build import *
from . import javabuiltins
from .class_factory import ClassFactory, NoSuchClass, default_class_factory
from .javacls import JavaClass
from .ser import Serializable
from .field import *
from .array import Array


def build_array(ary, factory=None):
    field = resolve_field(consts.TP_ARRAY, '', ary.desc.name, factory=factory)
    if field is None:
        raise TypeError('invalid array : %s' % obj.desc.name)
    return ary.data


def build_eunm(enum, factory=None):
    cls = JavaClass.resolve(obj.desc.name, factory=factory)
    if cls is None:
        raise TypeError('invalid enum : %s' % obj.desc.name)
    return cls(enum.value)
