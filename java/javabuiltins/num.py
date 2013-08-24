from ..javacls import JavaClass


class Number(JavaClass):
    __javaclass__ = 'java.lang.Number'


class Long(Number):
    __javaclass__ = 'java.lang.Long'

    def __repr__(self):
        return '%d' % self.value

    def __str__(self):
        return '%d' % self.value
