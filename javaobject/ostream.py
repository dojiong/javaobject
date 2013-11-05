from .java import consts
from .binary import BinWriter
from .blockdata import BlockDataWriter
from .reftable import ReferenceTable
from . import java
from functools import wraps
import six


def _add_ref(f):
    @wraps(f)
    def func(self, obj, *argv, **kwargv):
        idx = self._ref.reverse(obj)
        if idx != -1:
            self._write_reference(idx)
        else:
            f(self, obj, *argv, **kwargv)
    return func


Enum = java.JavaClass.resolve('java.lang.Enum')


class ObjectOStream:

    class WriteError(Exception):
        pass
    
    def __init__(self, f):
        self.__bin = BinWriter(f)
        self._ref = ReferenceTable()
        self.__write_table = {
            bool: self.write_bool,
            int: self.write_int,
            float: self.write_float,
            type(None): self.__write_null,
            type: self.__write_class,
            str: self.__write_string,
            java.Array: self.__write_array,
            object: self.__write_object,
            Exception: self.__write_exception,
        }
        if not six.PY3:
            self.__write_table[unicode] = self.__write_string
        self.__field_table = {
            consts.TP_BOOL: self.write_bool,
            consts.TP_BYTE: self.write_byte,
            consts.TP_CHAR: self.write_char,
            consts.TP_SHORT: self.write_short,
            consts.TP_INT: self.write_int,
            consts.TP_LONG: self.write_long,
            consts.TP_FLOAT: self.write_float,
            consts.TP_DOUBLE: self.write_double,
            consts.TP_OBJECT: self.__write_object,
            consts.TP_ARRAY: self.__write_array,
        }
        self.__write_head()

    def __write_head(self):
        self.__bin.ushort(consts.STREAM_MAGIC)
        self.__bin.ushort(consts.STREAM_VERSION)

    def write(self, obj):
        func = self.__write_table.get(type(obj), None)
        if func is not None:
            func(obj)
        elif isinstance(obj, java.JavaClass):
            self.__write_object(obj)
        else:
            raise self.WriteError('invalid type : %r' % type(obj))

    def write_bool(self, v, write_type=True):
        if write_type:
            self.__bin.byte(consts.TP_BOOL)
        self.__bin.byte(1) if v else self.__bin.byte(0)

    def write_byte(self, v, write_type=True):
        if write_type:
            self.__bin.byte(consts.TP_BYTE)
        self.__bin.byte(v)

    def write_char(self, v, write_type=True):
        if write_type:
            self.__bin.byte(consts.TP_CHAR)
        self.__bin.byte(ord(v))

    def write_short(self, v, write_type=True):
        if write_type:
            self.__bin.byte(consts.TP_SHORT)
        self.__bin.short(v)

    def write_int(self, v, write_type=True):
        if write_type:
            self.__bin.byte(consts.TP_INT)
        self.__bin.int32(v)

    def write_long(self, v, write_type=True):
        if write_type:
            self.__bin.byte(consts.TP_LONG)
        self.__bin.int64(v)

    def write_float(self, v, write_type=True):
        if write_type:
            self.__bin.byte(consts.TP_FLOAT)
        self.__bin.float(v)

    def write_double(self, v, write_type=True):
        if write_type:
            self.__bin.byte(consts.TP_DOUBLE)
        self.__bin.double(v)

    def __write_null(self, obj, write_type=True):
        self.__bin.byte(consts.TC_NULL)

    def _write_reference(self, idx, write_type=True):
        self.__bin.byte(consts.TC_REFERENCE)
        self.__bin.uint32(consts.baseWireHandle + idx)

    def __write_class(self, cls, write_type=True):
        self.__bin.byte(consts.TC_CLASS)
        self.__write_class_desc(cls)

    @_add_ref
    def __write_class_desc(self, cls, write_type=True):
        if not hasattr(cls, '__javaclass__'):
            raise self.WriteError('invalid JavaClass: %r' % cls)
        if hasattr(cls, '__classflag__'):
            clsflag = cls.__classflag__
        else:
            clsflag = consts.SC_SERIALIZABLE
            if issubclass(cls, java.Serializable):
                clsflag |= consts.SC_WRITE_METHOD
            if issubclass(cls, Enum):
                clsflag |= consts.SC_ENUM
        self.__bin.byte(consts.TC_CLASSDESC)
        self.__bin.utf(cls.__javaclass__)
        self.__bin.int64(cls.__suid__)
        self.__bin.byte(clsflag)
        self.__bin.ushort(len(cls.__fields__))
        self._ref.put(cls)
        for field in cls.__fields__.values():
            self.__bin.byte(field.typecode)
            self.__bin.utf(field.name)
            if field.typecode == consts.TP_ARRAY or \
                    field.typecode == consts.TP_OBJECT:
                idx = self._ref.reverse(field.signature)
                if idx != -1:
                    self._write_reference(idx)
                else:
                    self.__write_string(field.signature)
        self.__bin.byte(consts.TC_ENDBLOCKDATA)
        upper = None
        for base in cls.__bases__:
            if base == java.JavaClass:
                break
            elif issubclass(base, java.JavaClass):
                upper = base
        if upper == None:
            self.__bin.byte(consts.TC_NULL)
        else:
            self.__write_class_desc(upper)

    def __write_proxy_classDesc(self, obj, write_type=True):
        raise self.WriteError('unimplemented')

    def __write_string(self, s, write_type=True):
        if s is None:
            return self.__write_null(s)
        if len(s) <= 0xFFFF:
            self.__bin.byte(consts.TC_STRING)
            self.__bin.utf(s)
        else:
            self.__bin.byte(consts.TC_LONGSTRING)
            self.__bin.utf_long(s)
        self._ref.put(s)

    @_add_ref
    def __write_array(self, ary, write_type=True):
        if ary is None:
            return self.__write_null(ary)
        self.__bin.byte(consts.TC_ARRAY)
        self.__bin.byte(consts.TC_CLASSDESC)
        sig = ary.field.signature
        if callable(sig):
            sig = sig()
        self.__bin.utf('[' + sig.replace('/', '.'))
        self.__bin.int64(ary.__suid__)
        self.__bin.byte(2)
        self.__bin.ushort(0)
        self.__bin.byte(consts.TC_ENDBLOCKDATA)
        self.__bin.byte(consts.TC_NULL)

        self.__bin.uint32(len(ary))
        for e in ary:
            self.write(ary.field.__frompy__(e))

    @_add_ref
    def __write_enum(self, obj, write_type=True):
        pass

    def __write_object(self, obj, write_type=True):
        if isinstance(obj, six.string_types):
            return self.__write_string(obj)
        self.__bin.byte(consts.TC_OBJECT)
        self.__write_class_desc(type(obj))
        self._ref.put(obj)

        for k, field in obj.__fields__.items():
            val = getattr(obj, k)
            if val is None:
                self.__write_null(val)
            else:
                func = self.__field_table.get(field.typecode, None)
                if func is None:
                    raise self.WriteError('invalid object field')
                if not isinstance(val, field.type):
                    val = field.__frompy__(val)
                func(val, write_type=False)

        if isinstance(obj, java.Serializable):
            bd = BlockDataWriter()
            obj.encode(bd)
            self.__write_blockdata(bd)

        if issubclass(type(obj), Enum):
            self.__write_string(obj.value)

    def __write_exception(self, obj, write_type=True):
        raise self.WriteError('unimplemented')

    def __write_blockdata(self, bd, write_type=True):
        raw_size = bd.raw.tell()
        if raw_size > 0xFF:
            self.__bin.byte(consts.TC_BLOCKDATALONG)
            self.__bin.uint32(raw_size)
        else:
            self.__bin.byte(consts.TC_BLOCKDATA)
            self.__bin.byte(raw_size)
        self.__bin.write(bd.tobytes())
        for obj in bd.objects:
            self.write(obj)
        self.__bin.byte(consts.TC_ENDBLOCKDATA)
