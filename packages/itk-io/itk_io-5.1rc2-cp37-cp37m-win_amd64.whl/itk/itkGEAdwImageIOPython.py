# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.1
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _itkGEAdwImageIOPython
else:
    import _itkGEAdwImageIOPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkGEAdwImageIOPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkGEAdwImageIOPython.SWIG_PyStaticMethod_New

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import itkIPLCommonImageIOPython
import ITKIOImageBaseBasePython
import ITKCommonBasePython
import pyBasePython
import vnl_vectorPython
import vnl_matrixPython
import stdcomplexPython

def itkGEAdwImageIOFactory_New():
  return itkGEAdwImageIOFactory.New()


def itkGEAdwImageIO_New():
  return itkGEAdwImageIO.New()

class itkGEAdwImageIO(itkIPLCommonImageIOPython.itkIPLCommonImageIO):
    r"""Proxy of C++ itkGEAdwImageIO class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkGEAdwImageIOPython.itkGEAdwImageIO___New_orig__)
    Clone = _swig_new_instance_method(_itkGEAdwImageIOPython.itkGEAdwImageIO_Clone)
    __swig_destroy__ = _itkGEAdwImageIOPython.delete_itkGEAdwImageIO
    cast = _swig_new_static_method(_itkGEAdwImageIOPython.itkGEAdwImageIO_cast)

    def New(*args, **kargs):
        """New() -> itkGEAdwImageIO

        Create a new object of the class itkGEAdwImageIO and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkGEAdwImageIO.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkGEAdwImageIO.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkGEAdwImageIO.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkGEAdwImageIO in _itkGEAdwImageIOPython:
_itkGEAdwImageIOPython.itkGEAdwImageIO_swigregister(itkGEAdwImageIO)
itkGEAdwImageIO___New_orig__ = _itkGEAdwImageIOPython.itkGEAdwImageIO___New_orig__
itkGEAdwImageIO_cast = _itkGEAdwImageIOPython.itkGEAdwImageIO_cast

class itkGEAdwImageIOFactory(ITKCommonBasePython.itkObjectFactoryBase):
    r"""Proxy of C++ itkGEAdwImageIOFactory class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkGEAdwImageIOPython.itkGEAdwImageIOFactory___New_orig__)
    RegisterOneFactory = _swig_new_static_method(_itkGEAdwImageIOPython.itkGEAdwImageIOFactory_RegisterOneFactory)
    __swig_destroy__ = _itkGEAdwImageIOPython.delete_itkGEAdwImageIOFactory
    cast = _swig_new_static_method(_itkGEAdwImageIOPython.itkGEAdwImageIOFactory_cast)

    def New(*args, **kargs):
        """New() -> itkGEAdwImageIOFactory

        Create a new object of the class itkGEAdwImageIOFactory and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkGEAdwImageIOFactory.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkGEAdwImageIOFactory.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkGEAdwImageIOFactory.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkGEAdwImageIOFactory in _itkGEAdwImageIOPython:
_itkGEAdwImageIOPython.itkGEAdwImageIOFactory_swigregister(itkGEAdwImageIOFactory)
itkGEAdwImageIOFactory___New_orig__ = _itkGEAdwImageIOPython.itkGEAdwImageIOFactory___New_orig__
itkGEAdwImageIOFactory_RegisterOneFactory = _itkGEAdwImageIOPython.itkGEAdwImageIOFactory_RegisterOneFactory
itkGEAdwImageIOFactory_cast = _itkGEAdwImageIOPython.itkGEAdwImageIOFactory_cast



