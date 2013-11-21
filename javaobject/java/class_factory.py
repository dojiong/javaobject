
class NoSuchClass(Exception):
    pass


class LazyDescription(object):
    pass


class ClassFactory(object):
    def __init__(self, *supers):
        self.supers = supers
        self.classes = {}

    def __setitem__(self, clsname, cls):
        self.classes[clsname] = cls

    def __getitem__(self, clsname):
        if clsname in self.classes:
            return self.classes[clsname]
        for factory in self.supers:
            cls = factory.get(clsname, None)
            if cls is not None:
                return cls
        raise NoSuchClass(clsname)

    def get(self, clsname, *args, **kwargs):
        try:
            return self.__getitem__(clsname)
        except NoSuchClass:
            desc = kwargs.get('desc', None)
            if desc is not None:
                cls = self.build_class(desc)
                if cls is not None:
                    self.classes[clsname] = cls
                    return cls
            if len(args) == 0:
                raise
            elif len(args) == 1:
                return args[0]
            raise ValueError('invalid arguments: %r' % args)

    def set(self, clsname, cls):
        self.classes[clsname] = cls

    def build_class(self, desc):
        pass

    def build_object(self, obj, get_blockdata):
        from .ser import Serializable

        cls = self.get(obj.desc.name, desc=obj.desc)
        newobj = cls.__new__(cls)
        for k, field in cls.__fields__.items():
            setattr(newobj, k, obj.fields[field.name])
        if hasattr(newobj, '__build__') and callable(newobj.__build__):
            newobj.__build__(obj)

        if isinstance(newobj, Serializable):
            blockdata = get_blockdata()
            newobj.decode(blockdata)

        return newobj.__topy__()


default_class_factory = ClassFactory()
