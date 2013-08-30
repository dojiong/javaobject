from ..javacls import JavaClass
from ..field import *


class Number(JavaClass):
    __javaclass__ = 'java.lang.Number'
    __suid__ = -8742448824652078965


class Long(Number):
    __javaclass__ = 'java.lang.Long'
    __suid__ = 4290774380558885855

    value = LongField('value')

    def __init__(self, val=0):
        self.value = val

    def __repr__(self):
        return '%d' % self.value

    def __str__(self):
        return '%d' % self.value
