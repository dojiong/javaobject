from ..javacls import JavaClass


class Enum(JavaClass):
    __javaclass__ = 'java.lang.Enum'

    def __init__(self, value=None):
        self.value=value

    def __eq__(self, e):
        return self.value == e
