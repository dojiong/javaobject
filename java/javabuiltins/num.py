from ..javacls import JavaClass


class Number(JavaClass):
    __javaclass__ = 'java.lang.Number'


class Long(Number):
    __javaclass__ = 'java.lang.Long'
