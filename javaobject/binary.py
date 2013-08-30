from struct import pack, unpack


class BinReader:

    class ReadError(Exception):
        pass

    def __init__(self, flike):
        self.__f = flike
        # TODO: check f's binary mode

    def read(self, size):
        datas = []
        remain = size

        while remain > 0:
            try:
                data = self.__f.read(remain)
            except Exception as e:
                raise self.ReadError(e)
            if len(data) == 0:
                raise self.ReadError('read empty')
            datas.append(data)
            remain -= len(data)

        return b''.join(datas)

    def byte(self):
        return self.read(1)[0]

    def short(self):
        return unpack('>h', self.read(2))[0]

    def ushort(self):
        return unpack('>H', self.read(2))[0]

    def int32(self):
        return unpack('>i', self.read(4))[0]

    def uint32(self):
        return unpack('>I', self.read(4))[0]

    def int64(self):
        return unpack('>q', self.read(8))[0]

    def uint64(self):
        return unpack('>Q', self.read(8))[0]

    def float(self):
        return unpack('>f', self.read(4))[0]

    def double(self):
        return unpack('>d', self.read(8))[0]

    def utf(self):
        size = self.ushort()
        # TODO: UTF format
        return self.read(size).decode('UTF8')

    def utf_long(self):
        size = self.uint64()
        # TODO: UTF format
        return self.read(size).decode('UTF8')

    def is_equal(self, data):
        if isinstance(data, int):
            if data <= 0xFF:
                data = bytes([data])
            else:
                raise self.ReadError('invalid assert')
        if isinstance(data, str):
            data = data.encode('utf8')
        real = self.read(len(data))
        return real == data


class BinWriter:

    class WriteError(Exception):
        pass

    def __init__(self, flike):
        self.__f = flike
        # TODO: check f's binary mode

    def write(self, data):
        self.__f.write(data)

    def byte(self, data):
        self.write(bytes([data]))

    def short(self, data):
        self.write(pack('>h', data))

    def ushort(self, data):
        self.write(pack('>H', data))

    def int32(self, data):
        self.write(pack('>i', data))

    def uint32(self, data):
        self.write(pack('>I', data))

    def int64(self, data):
        self.write(pack('>q', data))

    def uint64(self, data):
        self.write(pack('>Q', data))

    def float(self, data):
        self.write(pack('>f', data))

    def double(self, data):
        self.write(pack('>d', data))

    def utf(self, s):
        # TODO: UTF format
        self.ushort(len(s))
        self.write(s.encode('UTF8'))

    def utf_long(self, s):
        # TODO: UTF format
        self.uint64(len(s))
        self.write(s.encode('UTF8'))
