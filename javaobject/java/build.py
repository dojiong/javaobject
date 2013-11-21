

class FieldDesc(object):
    __slots__ = 'typecode', 'name', 'signature'

    def __init__(self, typecode, name, signature):
        self.typecode = typecode
        self.name = name
        self.signature = signature

    def generate_field(self, factory=None):
        from .field import resolve_field
        return resolve_field(
            self.typecode, self.name, self.signature, factory)


class ClassDesc(object):
    __slots__ = 'name', 'suid', 'flag', 'fields', 'parent'

    def __init__(self, name=None, suid=None, flag=None, fields=None):
        self.name = name
        self.suid = suid
        self.flag = flag
        self.fields = fields
        self.parent = None

    def __repr__(self):
        return '<Class: %s>' % self.name

    def generate_class(self, factory=None):
        from .javacls import JavaClassMeta, JavaClass
        attrs = {'__javaclass__': self.name,
                 '__suid__': self.suid,
                 '__classflag__': self.flag}
        if factory is not None:
            attrs['__factory__'] = factory
        for field in self.fields:
            name = field.name.replace('$', '_')
            attrs[name] = field.generate_field(factory)
        return JavaClassMeta(self.name, (JavaClass, ), attrs)


class ArrayDesc(object):
    __slots__ = 'desc', 'data'

    def __init__(self, desc, data):
        self.desc = desc
        self.data = data

    def __repr__(self):
        return '[%s]' % self.desc.name[1:-1]


class EnumDesc(object):
    __slots__ = 'desc', 'value'

    def __init__(self, desc, value):
        self.desc = desc
        self.value = value

    def __repr__(self):
        return '<Enum: %s>' % self.value


class ObjectDesc(object):
    __slots__ = 'desc', 'fields'

    def __init__(self, desc, fields):
        self.desc = desc
        self.fields = fields

    def __repr__(self):
        return '<%s>' % self.desc.name

    def display(self):
        for field in self.desc.fields:
            print('\t%s: %r' % (field.name, self.fields[field.name]))

    def __getattr__(self, k):
        if k in self.fields:
            return self.fields[k]
        return super(ObjectDesc, self).__getattr__(k)
