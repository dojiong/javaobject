from ..javacls import JavaClass


class String(str, JavaClass):
    __javaclass__ = 'java.lang.String'
