from ..javacls import JavaClass
from ..ser import Serializable
from ..field import *


class Map(JavaClass):
    __javaclass__ = 'java.util.Map'
    __typecount__ = 2

    @classmethod
    def __frompy__(cls, *argv, **kwargv):
        return HashMap.__frompy__(*argv, **kwargv)


class HashMap(JavaClass, Serializable):
    __javaclass__ = 'java.util.HashMap'
    __suid__ = 362498820763181265
    __typecount__ = 2

    loadFactor = FloatField('loadFactor')
    threshold = IntField('threshold')

    def encode(self, bd):
        bd.uint32(0x10)
        bd.uint32(len(self.data))
        for k, v in self.data.items():
            bd.object(self.key_type.__frompy__(k))
            bd.object(self.value_type.__frompy__(v))

    def decode(self, bd):
        bd.uint32()
        size = bd.uint32()
        for i in range(size):
            k = bd.object()
            v = bd.object()
            self.data[k] = v

    def __build__(self, obj):
        self.data = {}

    def __topy__(self):
        return self.data

    @classmethod
    def __frompy__(cls, v, ktype, vtype):
        if isinstance(ktype, str):
            ktype = JavaClass.resolve(ktype)
        elif not issubclass(ktype, JavaClass):
            raise ValueError('invalid Map Key Type')
        if isinstance(vtype, str):
            vtype = JavaClass.resolve(vtype)
        elif not issubclass(vtype, JavaClass):
            raise ValueError('invalid Map Value Type')
        if isinstance(v, dict):
            return cls(ktype, vtype, v)
        raise ValueError('invalid HashMap')

    def __init__(self, ktype, vtype, dict=None, **kwargs):
        self.key_type = ktype
        self.value_type = vtype
        self.data = {}
        if dict is not None:
            self.data.update(dict)
        if len(kwargs):
            self.data.update(kwargs)
        self.loadFactor = 0x3f400000
        self.threshold = len(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)

    def __setitem__(self, key, item):
        self.data[key] = item

    def __delitem__(self, key):
        del self.data[key]
        self.threshold = len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, key):
        return key in self.data

    def __repr__(self):
        return repr(self.data)

    def copy(self):
        if self.__class__ is UserDict:
            return UserDict(self.data.copy())
        import copy
        data = self.data
        try:
            self.data = {}
            c = copy.copy(self)
        finally:
            self.data = data
        c.update(self)
        return c

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d
