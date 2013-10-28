from ..javacls import JavaClass
from ..ser import Serializable
from ..field import *
from datetime import datetime


class Date(JavaClass, Serializable):
    __javaclass__ = 'java.util.Date'

    def __init__(self):
        self.timestamp = 0

    def encode(self, bd):
        bd.uint64(timestamp)

    def decode(self, bd):
        self.timestamp = bd.uint64() / 1000.0

    def __topy__(self):
        return datetime.fromtimestamp(self.timestamp)
