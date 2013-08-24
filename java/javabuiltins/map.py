from ..javacls import JavaClass
from ..ser import Serializable


class HashMap(JavaClass, Serializable):
    __javaclass__ = 'java.util.HashMap'

    def __init__(self):
        self.map = {}

    def encode(self, bd):
        pass

    def decode(self, bd):
        bd.uint32()
        size = bd.uint32()
        for i in range(size):
            k = bd.object()
            v = bd.object()
            self.map[k] = v
