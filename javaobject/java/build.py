
class ClassDesc(object):

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
            attrs[name] = field
        return JavaClassMeta(self.name, (JavaClass, ), attrs)


class ArrayDesc(object):

    def __init__(self, desc, data):
        self.desc = desc
        self.data = data

    def __repr__(self):
        return '[%s]' % self.desc.name[1:-1]


class EnumDesc(object):

    def __init__(self, desc, value):
        self.desc = desc
        self.value = value

    def __repr__(self):
        return '<Enum: %s>' % self.value


class ObjectDesc(object):

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
        print(ObjectDesc, self)
        return super(ObjectDesc, self).__getattr__(k)
