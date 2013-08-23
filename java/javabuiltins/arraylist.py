from ..javacls import JavaClass
from ..ser import Serializable


class ArrayList(JavaClass, Serializable):
    __javaclass__ = 'java.util.ArrayList'

    def __init__(self):
        self.array = []

    def encode(self, bd):
        pass

    def decode(self, bd):
        size = bd.uint32()
        for i in range(size):
            self.array.append(bd.object())
