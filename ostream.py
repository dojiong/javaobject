from java import consts
from binary import BinWriter
from blockdata import BlockDataWriter
from reftable import ReferenceTable
import java
from functools import wraps


def _add_ref(f):
    @wraps(f)
    def func(self, obj):
        if not hasattr(obj, '__hash__') or obj.__hash__ is None:
            return f(self, obj)
        idx = self._ref.reverse(obj)
        if idx != -1:
            self._write_reference(idx)
        else:
            f(self, obj)
    return func


Enum = java.JavaClass.resolve('java.lang.Enum')


class ObjectOStream:

    class WriteError(Exception):
        pass
    
    def __init__(self, f):
        self.__bin = BinWriter(f)
        self._ref = ReferenceTable()
        self.write_bool = lambda x: self.__bin.byte(1) if x else self.__bin.byte(0)
        self.write_byte = self.__bin.byte
        self.write_char = lambda x: self.__bin.byte(ord(x))
        self.write_short = self.__bin.short
        self.write_int = self.__bin.int32
        self.write_long = self.__bin.int64
        self.write_float = self.__bin.float
        self.write_double = self.__bin.double
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

    def __write_null(self, obj):
        self.__bin.byte(consts.TC_NULL)

    def _write_reference(self, idx):
        self.__bin.byte(consts.TC_REFERENCE)
        self.__bin.uint32(consts.baseWireHandle + idx)

    def __write_class(self, cls):
        self.__bin.byte(consts.TC_CLASS)
        self.__write_class_desc(cls)

    @_add_ref
    def __write_class_desc(self, cls):
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

    def __write_proxy_classDesc(self, obj):
        raise self.WriteError('unimplemented')

    @_add_ref
    def __write_string(self, s):
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
    def __write_array(self, ary):
        if ary is None:
            return self.__write_null(ary)
        self.__bin.byte(consts.TC_ARRAY)
        self.__bin.byte(consts.TC_CLASSDESC)
        self.__bin.utf('[' + ary.field.signature.replace('/', '.'))
        self.__bin.int64(ary.__suid__)
        self.__bin.byte(2)
        self.__bin.ushort(0)
        self.__bin.byte(consts.TC_ENDBLOCKDATA)
        self.__bin.byte(consts.TC_NULL)

        self.__bin.uint32(len(ary))
        func = self.__field_table.get(ord(ary.field.signature[0]), None)
        if func is None:
            print(ary.field.signature)
            raise self.WriteError('invalid array field')
        for e in ary:
            func(e)

    @_add_ref
    def __write_enum(self, obj):
        pass

    def __write_object(self, obj):
        if isinstance(obj, str):
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
                func(val)

        if isinstance(obj, java.Serializable):
            bd = BlockDataWriter()
            obj.encode(bd)
            self.__write_blockdata(bd)

    def __write_exception(self, obj):
        raise self.WriteError('unimplemented')

    def __write_blockdata(self, bd):
        raw_size = bd.raw.tell()
        if raw_size > 0xFF:
            self.__bin.byte(consts.TC_BLOCKDATALONG)
            self.__bin.uint32(raw_size)
        else:
            self.__bin.byte(consts.TC_BLOCKDATA)
            self.__bin.byte(raw_size)
        self.__bin.write(bd.raw.getbuffer().tobytes())
        for obj in bd.objects:
            self.write(obj)
        self.__bin.byte(consts.TC_ENDBLOCKDATA)
