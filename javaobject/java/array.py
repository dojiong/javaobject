


class Array(object):

    def __init__(self, field, initlist=None, suid=0):
        from .javabuiltins.arraylist import ArrayList

        self.field = field
        self.__suid__ = suid
        self.data = []
        if initlist is not None:
            if isinstance(initlist, type(self.data)):
                self.data[:] = initlist
            elif isinstance(initlist, ArrayList):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)

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

    def __iter__(self):
        return iter(self.data)

    def append(self, item):
        self.data.append(item)

    def insert(self, i, item):
        self.data.insert(i, item)

    def pop(self, i=-1):
        return self.data.pop(i)

    def remove(self, item):
        self.data.remove(item)

    def clear(self):
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
        from .javabuiltins.arraylist import ArrayList

        if isinstance(other, ArrayList):
            self.data.extend(other.data)
        else:
            self.data.extend(other)
