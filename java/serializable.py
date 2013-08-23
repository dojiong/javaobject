

class SerializableMeta(type):
    def __new__(self, name, bases, clsdict):
        if '__javaclass__' not in clsdict:
            raise TypeError('missing __javaclass__')
        if clsdict['__javaclass__'] != 'java.io.Serializable':
            if not callable(clsdict.get('encode', None)):
                raise TypeError('missing encode')
            if not callable(clsdict.get('decode', None)):
                raise TypeError('missing decode')
        cls = type.__new__(self, name, bases, clsdict)
        cls._classes[clsdict['__javaclass__']] = cls
        return cls


class Serializable(metaclass=SerializableMeta):
    _classes = {}
    __javaclass__ = 'java.io.Serializable'

    @classmethod
    def get_class(cls, name):
        return cls._classes.get(name, None)
