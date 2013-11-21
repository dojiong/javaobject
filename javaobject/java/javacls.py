from .field import BaseField
from collections import OrderedDict
from .prepareable import Prepareable
from .class_factory import ClassFactory, default_class_factory
import six


class JavaClassMeta(six.with_metaclass(Prepareable, type)):
    def __prepare__(name, bases):
        return OrderedDict()

    def __new__(self, name, bases, attrs):
        if '__javaclass__' not in attrs:
            raise TypeError('missing __javaclass__')

        fields = OrderedDict()
        for key, field in attrs.items():
            if isinstance(field, BaseField):
                fields[key] = field
                if callable(field.default):
                    attrs[key] = field.default()
                else:
                    attrs[key] = field.default
        attrs['__fields__'] = fields
        if '__suid__' not in attrs:
            attrs['__suid__'] = 0
        if '__classflag__' in attrs and attrs['__classflag__'] > 0xFF:
            raise TypeError('invalid class flag: 0x%X' % attrs['__classflag__'])
        if '__factory__' in attrs:
            factory = attrs['__factory__'] or default_class_factory
            if not isinstance(factory, ClassFactory):
                raise TypeError('invalid __factory__')
        else:
            factory = default_class_factory

        cls = type.__new__(self, name, bases, attrs)
        factory[attrs['__javaclass__']] = cls
        return cls


@six.add_metaclass(JavaClassMeta)
class JavaClass(object):
    __javaclass__ = 'Java'

    @classmethod
    def resolve(cls, name, desc=None, lazy=False, factory=None):
        if name[0] == 'L' and name[-1] == ';':
            name = name[1:-1]
            if name.find('.') == -1:
                name = name.replace('/', '.')
        if factory is None:
            factory = default_class_factory
        return factory.get(name, lazy=lazy, desc=desc)

    @classmethod
    def signature(cls):
        return 'L%s;' % cls.__javaclass__.replace('.', '/')

    def __topy__(self):
        return self

    @classmethod
    def __frompy__(self, v):
        return v

    def copyfrom(self, obj):
        if not isinstance(obj, type(self)):
            raise ValueError('type not equal')
        for k, field in self.__fields__.items():
            setattr(self, k, getattr(obj, k))
