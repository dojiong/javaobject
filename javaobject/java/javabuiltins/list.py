from ..javacls import JavaClass


class List(JavaClass):
    __javaclass__ = 'java.util.List'
    __typecount__ = 1

    @classmethod
    def __frompy__(cls, *argv, **kwargv):
        ArrayList = JavaClass.resolve('java.util.ArrayList')
        return ArrayList.__frompy__(*argv, **kwargv)
