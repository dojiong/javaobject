from ..javacls import JavaClass
from ..ser import Serializable
from ..field import *


class Map(JavaClass):
    __javaclass__ = 'java.util.Map'


class HashMap(JavaClass, Serializable):
    __javaclass__ = 'java.util.HashMap'
    __suid__ = 362498820763181265
    __classflag__ = 3

    loadFactor = FloatField('loadFactor')
    threshold = IntField('threshold')

    def encode(self, bd):
        bd.uint32(0x10)
        bd.uint32(len(self.data))
        for k, v in self.data.items():
            bd.object(k)
            bd.object(v)

    def decode(self, bd):
        bd.uint32()
        size = bd.uint32()
        for i in range(size):
            k = bd.object()
            v = bd.object()
            self.data[k] = v

    def __build__(self, obj):
        self.data = {}

    def __init__(self, dict=None, **kwargs):
        self.data = {}
        if dict is not None:
            self.update(dict)
        if len(kwargs):
            self.update(kwargs)

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
