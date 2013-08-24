from . import consts

class BaseField(object):
    def __init__(self, name):
        super(BaseField, self).__init__()
        self.name = name
        self.type = self.__class__

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)


class BoolField(BaseField):
    typecode = consts.TP_BOOL
    signature = consts.TP_BOOL


class ByteField(BaseField):
    typecode = consts.TP_BYTE
    signature = consts.TP_BYTE


class CharField(BaseField):
    typecode = consts.TP_CHAR
    signature = consts.TP_CHAR


class ShortField(BaseField):
    typecode = consts.TP_SHORT
    signature = consts.TP_SHORT


class IntField(BaseField):
    typecode = consts.TP_INT
    signature = consts.TP_INT


class LongField(BaseField):
    typecode = consts.TP_LONG
    signature = consts.TP_LONG


class FloatField(BaseField):
    typecode = consts.TP_FLOAT
    signature = consts.TP_FLOAT


class DoubleField(BaseField):
    typecode = consts.TP_DOUBLE
    signature = consts.TP_DOUBLE


class ArrayField(BaseField):
    typecode = consts.TP_ARRAY
    signature = consts.TP_ARRAY

    def __init__(self, name, t):
        self.ele_type = t
        super(ArrayField, self).__init__(name)


class ObjectField(BaseField):
    typecode = consts.TP_OBJECT

    def __init__(self, name, t):
        super(ObjectField, self).__init__(name)
        self.type = t
        self.signature = t.signature()


class InvalidField(Exception):
    pass

builtin_types = {
    consts.TP_BOOL: BoolField,
    consts.TP_BYTE: ByteField,
    consts.TP_CHAR: CharField,
    consts.TP_SHORT: ShortField,
    consts.TP_INT: IntField,
    consts.TP_LONG: LongField,
    consts.TP_FLOAT: FloatField,
    consts.TP_DOUBLE: DoubleField,
    consts.TP_ARRAY: ArrayField}


def resolve_field(t, name, signature):
    from .javacls import JavaClass
    if t == consts.TP_OBJECT:
        if signature[0] != 'L' or signature[-1] != ';':
            raise InvalidField('invalid object signature')
        return ObjectField(name, JavaClass.resolve(signature))
    elif t == consts.TP_ARRAY:
        if signature[0] != '[':
            raise InvalidField('invalid array signature')
        internal = resolve_field(ord(signature[1]), '$E', signature[1:])
        return ArrayField(name, internal.type)
    cls = builtin_types.get(t, None)
    if cls is None:
        raise InvalidField('invalid type: %x' % t)
    return cls(name)


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
        return super(Object, self).__getattr__(k)
