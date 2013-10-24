from .java import consts
from .binary import BinReader
from .reftable import ReferenceTable
from . import java
from .blockdata import BlockDataReader
import six


class ObjectIStream:

    class ReadError(Exception):
        pass

    def __init__(self, f):
        self.__bin = BinReader(f)
        self.__ref = ReferenceTable()
        self.__read_map = {
            consts.TC_NULL: self.__read_null,
            consts.TC_REFERENCE: self.__read_reference,
            consts.TC_CLASS: self.__read_class,
            consts.TC_CLASSDESC: self.__read_class_desc,
            consts.TC_PROXYCLASSDESC: self.__read_proxy_classDesc,
            consts.TC_STRING: self.__read_string,
            consts.TC_LONGSTRING: self.__read_long_string,
            consts.TC_ARRAY: self.__read_array,
            consts.TC_ENUM: self.__read_enum,
            consts.TC_OBJECT: self.__read_object,
            consts.TC_EXCEPTION: self.__read_exception,
            consts.TC_BLOCKDATA: self.__read_blockdata,
            consts.TC_BLOCKDATALONG: self.__readblockdata_long,
            consts.TP_BOOL: self.read_bool,
            consts.TP_BYTE: self.read_byte,
            consts.TP_CHAR: self.read_char,
            consts.TP_SHORT: self.read_short,
            consts.TP_INT: self.read_int,
            consts.TP_LONG: self.read_long,
            consts.TP_FLOAT: self.read_float,
            consts.TP_DOUBLE: self.read_double,
            consts.TP_OBJECT: self.read,
            consts.TP_ARRAY: self.read,
        }
        self.__check_head()

    def read(self):
        t = self.__bin.byte()
        return self.__read_hint(t)

    def __check_head(self):
        magic = self.__bin.ushort()
        version = self.__bin.ushort()
        if magic != consts.STREAM_MAGIC:
            raise self.ReadError('invalid magic: 0x%x' % magic)
        if version != consts.STREAM_VERSION:
            raise self.ReadError('unsupported version: %d' % version)

    def __read_hint(self, t):
        func = self.__read_map.get(t, None)
        if func is None:
            raise self.ReadError('invalid type: 0x%X' % t)
        try:
            return func()
        except BinReader.ReadError as e:
            raise self.ReadError(e)

    def read_bool(self):
        return self.__bin.byte() != 0

    def read_byte(self):
        return self.__bin.byte()

    def read_char(self):
        return chr(self.__bin.byte())

    def read_short(self):
        return self.__bin.short()

    def read_int(self):
        return self.__bin.int32()

    def read_long(self):
        return self.__bin.int64()

    def read_float(self):
        return self.__bin.float()

    def read_double(self):
        return self.__bin.double()

    def __read_null(self):
        return None

    def __read_reference(self):
        idx = self.__bin.uint32()
        idx -= consts.baseWireHandle
        try:
            return self.__ref.get(idx)
        except self.__ref.NotFound:
            raise self.ReadError('invalid reference: %d' % idx)

    def __read_class(self):
        if not self.__bin.is_equal(consts.TC_CLASSDESC):
            raise self.ReadError('Class: ClassDesc required')
        return self.__read_class_desc()

    def __read_class_desc(self):
        name = self.__bin.utf()
        suid = self.__bin.int64()
        flag = self.__bin.byte()
        fields_size = self.__bin.ushort()
        desc = java.ClassDesc(name, suid, flag, [])
        self.__ref.put(desc)
        for i in range(fields_size):
            t = self.__bin.byte()
            name = self.__bin.utf()
            if t == consts.TP_OBJECT or t == consts.TP_ARRAY:
                signature = self.read()
                if not isinstance(signature, six.text_type):
                    raise self.ReadError(
                        'invalid TypeString (field: %s)' % name)
            else:
                signature = t
            desc.fields.append(java.resolve_field(t, name, signature))
        if not self.__bin.is_equal(consts.TC_ENDBLOCKDATA):
            raise self.ReadError('invalid ClassDesc end')
        next = self.read()
        if not isinstance(next, (type(None), java.ClassDesc)):
            raise self.ReadError('invalid parent class for %s' % name)
        desc.parent = next
        return desc

    def __read_proxy_classDesc(self):
        raise self.ReadError('unimplemented')

    def __read_string(self):
        s = self.__bin.utf()
        self.__ref.put(s)
        return s

    def __read_long_string(self):
        s = self.__bin.utfLong()
        self.__ref.put(s)
        return s

    def __read_array(self):
        desc = self.read()
        if not isinstance(desc, (type(None), java.ClassDesc)):
            raise self.ReadError('invalid array description')
        ary = java.ArrayDesc(desc, [])
        idx = self.__ref.put(ary)

        for i in range(self.__bin.uint32()):
            ary.data.append(self.read())

        newary = java.build_array(ary)
        self.__ref.replace(idx, newary)
        return newary

    def __read_enum(self):
        desc = self.read()
        if not isinstance(desc, (type(None), java.ClassDesc)):
            raise self.ReadError('invalid enum description')
        enum = java.EnumDesc(desc, '')
        val = self.read()
        if not isinstance(val, str):
            raise self.ReadError('invalid enum value')
        enum.value = val

        enum = java.build_enum(enum)
        self.__ref.put(enum)
        return enum

    def __read_object(self):
        desc = self.read()
        if not isinstance(desc, (type(None), java.ClassDesc)):
            raise self.ReadError('invalid object description')
        obj = java.ObjectDesc(desc, {})
        idx = self.__ref.put(obj)

        for field in desc.fields:
            obj.fields[field.name] = self.__read_hint(field.typecode)

        newobj = java.build_object(obj, self.__get_blockdata)
        self.__ref.replace(idx, newobj)
        return newobj

    def __get_blockdata(self):
        bd = self.read()
        if not isinstance(bd, BlockDataReader):
            raise self.ReadError('missing blockdata')
        return bd        

    def __read_exception(self):
        raise self.ReadError('unimplemented')

    def __read_blockdata(self):
        raw_size = self.__bin.byte()
        return self.__read_blockdata0(raw_size)

    def __readblockdata_long(self):
        raw_size = self.__bin.uint32()
        return self.__read_blockdata0(raw_size)

    def __read_blockdata0(self, raw_size):
        raw = self.__bin.read(raw_size)
        objs = []

        while True:
            t = self.__bin.byte()
            if t == consts.TC_ENDBLOCKDATA:
                break
            objs.append(self.__read_hint(t))

        return BlockDataReader(raw, objs)
