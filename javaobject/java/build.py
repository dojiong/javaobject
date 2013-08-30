
class ClassDesc:

    def __init__(self, name=None, suid=None, flag=None, fields=None):
        self.name = name
        self.suid = suid
        self.flag = flag
        self.fields = fields
        self.parent = None

    def __repr__(self):
        return '<Class: %s>' % self.name


class ArrayDesc:

    def __init__(self, desc, data):
        self.desc = desc
        self.data = data

    def __repr__(self):
        return '[%s]' % self.desc.name[1:-1]


class EnumDesc:

    def __init__(self, desc, value):
        self.desc = desc
        self.value = value

    def __repr__(self):
        return '<Enum: %s>' % self.value


class ObjectDesc:

    def __init__(self, desc, fields):
        self.desc = desc
        self.fields = fields

    def __repr__(self):
        return '<%s>' % self.desc.name

    def display(self):
        print('Class:', self.desc.name)
        for field in self.desc.fields:
            print('\t%s: %r' % (field.name, self.fields[field.name]))

    def __getattr__(self, k):
        if k in self.fields:
            return self.fields[k]
        return super(ObjectDesc, self).__getattr__(k)
