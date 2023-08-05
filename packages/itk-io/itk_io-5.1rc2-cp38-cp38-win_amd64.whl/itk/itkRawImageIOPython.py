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
    from . import _itkRawImageIOPython
else:
    import _itkRawImageIOPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkRawImageIOPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkRawImageIOPython.SWIG_PyStaticMethod_New

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


import ITKCommonBasePython
import pyBasePython
import ITKIOImageBaseBasePython
import vnl_vectorPython
import stdcomplexPython
import vnl_matrixPython

def itkRawImageIOF3_New():
  return itkRawImageIOF3.New()


def itkRawImageIOF2_New():
  return itkRawImageIOF2.New()

class itkRawImageIOF2(ITKIOImageBaseBasePython.itkImageIOBase):
    r"""Proxy of C++ itkRawImageIOF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRawImageIOPython.itkRawImageIOF2___New_orig__)
    Clone = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF2_Clone)
    SetHeaderSize = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF2_SetHeaderSize)
    GetHeaderSize = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF2_GetHeaderSize)
    SetFileDimensionality = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF2_SetFileDimensionality)
    GetFileDimensionality = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF2_GetFileDimensionality)
    GetImageMask = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF2_GetImageMask)
    SetImageMask = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF2_SetImageMask)
    ReadHeader = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF2_ReadHeader)
    __swig_destroy__ = _itkRawImageIOPython.delete_itkRawImageIOF2
    cast = _swig_new_static_method(_itkRawImageIOPython.itkRawImageIOF2_cast)

    def New(*args, **kargs):
        """New() -> itkRawImageIOF2

        Create a new object of the class itkRawImageIOF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRawImageIOF2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRawImageIOF2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRawImageIOF2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRawImageIOF2 in _itkRawImageIOPython:
_itkRawImageIOPython.itkRawImageIOF2_swigregister(itkRawImageIOF2)
itkRawImageIOF2___New_orig__ = _itkRawImageIOPython.itkRawImageIOF2___New_orig__
itkRawImageIOF2_cast = _itkRawImageIOPython.itkRawImageIOF2_cast

class itkRawImageIOF3(ITKIOImageBaseBasePython.itkImageIOBase):
    r"""Proxy of C++ itkRawImageIOF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRawImageIOPython.itkRawImageIOF3___New_orig__)
    Clone = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF3_Clone)
    SetHeaderSize = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF3_SetHeaderSize)
    GetHeaderSize = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF3_GetHeaderSize)
    SetFileDimensionality = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF3_SetFileDimensionality)
    GetFileDimensionality = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF3_GetFileDimensionality)
    GetImageMask = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF3_GetImageMask)
    SetImageMask = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF3_SetImageMask)
    ReadHeader = _swig_new_instance_method(_itkRawImageIOPython.itkRawImageIOF3_ReadHeader)
    __swig_destroy__ = _itkRawImageIOPython.delete_itkRawImageIOF3
    cast = _swig_new_static_method(_itkRawImageIOPython.itkRawImageIOF3_cast)

    def New(*args, **kargs):
        """New() -> itkRawImageIOF3

        Create a new object of the class itkRawImageIOF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRawImageIOF3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRawImageIOF3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRawImageIOF3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRawImageIOF3 in _itkRawImageIOPython:
_itkRawImageIOPython.itkRawImageIOF3_swigregister(itkRawImageIOF3)
itkRawImageIOF3___New_orig__ = _itkRawImageIOPython.itkRawImageIOF3___New_orig__
itkRawImageIOF3_cast = _itkRawImageIOPython.itkRawImageIOF3_cast



