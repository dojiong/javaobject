from .build import *
from . import javabuiltins
from .javacls import JavaClass
from .ser import Serializable


def build_object(obj, get_blockdata):
    cls = JavaClass.get_class(obj.desc.name)
    if cls is None:
        raise TypeError('invalid class : %s' % obj.desc.name)
    newobj = cls()
    for field in obj.desc.fields:
        setattr(newobj, field.name, obj.fields[field.name])

    if isinstance(newobj, Serializable):
        blockdata = get_blockdata()
        newobj.decode(blockdata)

    return newobj
