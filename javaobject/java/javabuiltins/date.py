from ..javacls import JavaClass
from ..ser import Serializable
from ..field import *
from datetime import datetime
import six
import time


class Date(JavaClass, Serializable):
    __javaclass__ = 'java.util.Date'
    __suid__ = 7523967970034938905

    def __init__(self, timestamp=0):
        self.timestamp = timestamp

    def encode(self, bd):
        bd.uint64(int(self.timestamp * 1000))

    def decode(self, bd):
        self.timestamp = bd.uint64() / 1000.0

    def __topy__(self):
        return datetime.fromtimestamp(self.timestamp)

    @classmethod
    def __frompy__(cls, v):
        if isinstance(v, datetime):
            if six.PY3:
                return cls(v.timestamp())
            return cls(time.mktime(v.timetuple()))
        elif isinstance(v, six.integer_types):
            return cls(v)
        raise ValueError('invalid Date')
