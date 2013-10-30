from ..javacls import JavaClass
from ..ser import Serializable
from ..field import IntField


class ArrayList(JavaClass, Serializable):
    __javaclass__ = 'java.util.ArrayList'
    __suid__ = 8683452581122892189

    size = IntField('size')

    def encode(self, bd):
        bd.uint32(len(self.data) * 2)
        for ele in self.data:
            bd.object(ele)

    def decode(self, bd):
        cap = bd.uint32()
        for i in range(self.size):
            obj = bd.object()
            self.data.append(obj)

    def __build__(self, obj):
        self.data = []

    def __topy__(self):
        return self.data

    @classmethod
    def __frompy__(cls, v):
        if isinstance(v, list):
            return cls(v)
        elif isinstance(v, tuple):
            return cls(v)
        raise ValueError('invalid ArrayList')

    def __init__(self, initlist=None):
        self.data = []
        if initlist is not None:
            if isinstance(initlist, type(self.data)):
                self.data[:] = initlist
            elif isinstance(initlist, ArrayList):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)
        self.size = len(self.data)

    def __repr__(self):
        return repr(self.data)

    def __contains__(self, item):
        return item in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, i, item):
        self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]
        self.size = len(self.data)

    def __add__(self, other):
        self.size += len(other)
        if isinstance(other, ArrayList):
            return self.__class__(self.data + other.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(self.data + other)
        rst = self.__class__(self.data + list(other))
        self.size = len(self.data)
        return rst

    def __radd__(self, other):
        self.size += len(other)
        if isinstance(other, ArrayList):
            return self.__class__(other.data + self.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(other + self.data)
        rst = self.__class__(list(other) + self.data)
        self.size = len(self.data)
        return rst

    def __iadd__(self, other):
        self.size += len(other)
        if isinstance(other, ArrayList):
            self.data += other.data
        elif isinstance(other, type(self.data)):
            self.data += other
        else:
            self.data += list(other)
        self.size = len(self.data)
        return self

    def __mul__(self, n):
        rst = self.__class__(self.data * n)
        self.size = len(self.data)
        return rst
    __rmul__ = __mul__

    def __imul__(self, n):
        self.data *= n
        self.size = len(self.data)
        return self

    def append(self, item):
        self.data.append(item)
        self.size = len(self.data)

    def insert(self, i, item):
        self.data.insert(i, item)
        self.size = len(self.data)

    def pop(self, i=-1):
        self.size -= 1
        return self.data.pop(i)

    def remove(self, item):
        self.size -= 1
        self.data.remove(item)

    def clear(self):
        self.size = 0
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self.data.count(item)

    def index(self, item, *args):
        return self.data.index(item, *args)

    def reverse(self):
        self.data.reverse()

    def sort(self, *args, **kwds):
        self.data.sort(*args, **kwds)

    def extend(self, other):
        if isinstance(other, ArrayList):
            self.data.extend(other.data)
        else:
            self.data.extend(other)
        self.size = len(self.data)
