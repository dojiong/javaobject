from ..javacls import JavaClass


class List(JavaClass):
    __javaclass__ = 'java.util.List'

    @classmethod
    def __frompy__(cls, v):
        ArrayList = JavaClass.resolve('java.util.ArrayList')
        if isinstance(v, list):
            return ArrayList(v)
        elif isinstance(v, tuple):
            return ArrayList(v)
        raise ValueError('invalid List')
