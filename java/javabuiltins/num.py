from ..javacls import JavaClass
from ..field import *


class Number(JavaClass):
    __javaclass__ = 'java.lang.Number'


class Long(Number):
    __javaclass__ = 'java.lang.Long'

    value = LongField('value')

    def __repr__(self):
        return '%d' % self.value

    def __str__(self):
        return '%d' % self.value
