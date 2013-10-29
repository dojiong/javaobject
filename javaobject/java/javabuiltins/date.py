from ..javacls import JavaClass
from ..ser import Serializable
from ..field import *
from datetime import datetime
import six


class Date(JavaClass, Serializable):
    __javaclass__ = 'java.util.Date'

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
            return cls(v.timestamp())
        elif isinstance(v, six.integer_types):
            return cls(v)
        raise ValueError('invalid Date')
