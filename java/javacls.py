

class JavaClassMeta(type):
    def __new__(self, name, bases, clsdict):
        if '__javaclass__' not in clsdict:
            raise TypeError('missing __javaclass__')
        cls = type.__new__(self, name, bases, clsdict)
        cls._classes[clsdict['__javaclass__']] = cls
        return cls


class JavaClass(metaclass=JavaClassMeta):
    _classes = {}
    __javaclass__ = 'Java'

    class InvalidClass(Exception):
        pass

    @classmethod
    def resolve(cls, name):
        if name[0] == 'L' and name[-1] == ';':
            name = name[1:-1]
            if name.find('.') == -1:
                name = name.replace('/', '.')
        rst = cls._classes.get(name, None)
        if rst is None:
            raise cls.InvalidClass('can\'t find %r' % name)
        return rst

    @classmethod
    def signature(cls):
        return 'L%s;' % cls.__javaclass__.replace('.', '/')
