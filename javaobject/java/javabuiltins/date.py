from ..javacls import JavaClass
from ..ser import Serializable
from ..field import *


class Date(JavaClass, Serializable):
    __javaclass__ = 'java.util.Date'

    def __init__(self):
        self.timestamp = 0

    def encode(self, bd):
        bd.uint64(timestamp)

    def decode(self, bd):
        self.timestamp = bd.uint64() / 1000.0
