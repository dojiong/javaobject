

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

    @classmethod
    def get_class(cls, name):
        return cls._classes.get(name, None)
