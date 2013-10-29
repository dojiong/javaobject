from ..javacls import JavaClass
from ..field import *
import six


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

    def __eq__(self, n):
        return self.value == n

    def __topy__(self):
        return self.value

    @classmethod
    def __frompy__(cls, v):
        if not isinstance(v, six.integer_types):
            raise ValueError('integer required')
        return cls(v)


class Integer(Number):
    __javaclass__ = 'java.lang.Integer'
    __suid__ = 1360826667806852920

    value = IntField('value')

    def __init__(self, val=0):
        self.value = val

    def __repr__(self):
        return '%d' % self.value

    def __str__(self):
        return '%d' % self.value

    def __eq__(self, n):
        return self.value == n

    def __topy__(self):
        return self.value

    @classmethod
    def __frompy__(cls, v):
        if not isinstance(v, six.integer_types):
            raise ValueError('integer required')
        return cls(v)
