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
    default = False


class ByteField(BaseField):
    typecode = consts.TP_BYTE
    signature = consts.TP_BYTE
    default = 0


class CharField(BaseField):
    typecode = consts.TP_CHAR
    signature = consts.TP_CHAR
    default = '\x00'


class ShortField(BaseField):
    typecode = consts.TP_SHORT
    signature = consts.TP_SHORT
    default = 0


class IntField(BaseField):
    typecode = consts.TP_INT
    signature = consts.TP_INT
    default = 0


class LongField(BaseField):
    typecode = consts.TP_LONG
    signature = consts.TP_LONG
    default = 0


class FloatField(BaseField):
    typecode = consts.TP_FLOAT
    signature = consts.TP_FLOAT
    default = 0.0


class DoubleField(BaseField):
    typecode = consts.TP_DOUBLE
    signature = consts.TP_DOUBLE
    default = 0.0


class ArrayField(BaseField):
    typecode = consts.TP_ARRAY
    signature = consts.TP_ARRAY
    default = []

    def __init__(self, name, t):
        self.ele_type = t
        super(ArrayField, self).__init__(name)


class ObjectField(BaseField):
    typecode = consts.TP_OBJECT
    default = None

    def __init__(self, name, t):
        from .javacls import JavaClass
        super(ObjectField, self).__init__(name)
        if isinstance(t, str):
            t = JavaClass.resolve(t)
        self.type = t
        self.signature = t.signature()


class StringField(ObjectField):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'java.lang.String')


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
