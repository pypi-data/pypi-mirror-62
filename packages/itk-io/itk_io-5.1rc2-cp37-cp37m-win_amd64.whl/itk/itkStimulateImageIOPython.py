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
    from . import _itkStimulateImageIOPython
else:
    import _itkStimulateImageIOPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkStimulateImageIOPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkStimulateImageIOPython.SWIG_PyStaticMethod_New

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
import vnl_matrixPython
import stdcomplexPython

def itkStimulateImageIOFactory_New():
  return itkStimulateImageIOFactory.New()


def itkStimulateImageIO_New():
  return itkStimulateImageIO.New()

class itkStimulateImageIO(ITKIOImageBaseBasePython.itkImageIOBase):
    r"""Proxy of C++ itkStimulateImageIO class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkStimulateImageIOPython.itkStimulateImageIO___New_orig__)
    Clone = _swig_new_instance_method(_itkStimulateImageIOPython.itkStimulateImageIO_Clone)
    GetDisplayRange = _swig_new_instance_method(_itkStimulateImageIOPython.itkStimulateImageIO_GetDisplayRange)
    GetHighDisplayValue = _swig_new_instance_method(_itkStimulateImageIOPython.itkStimulateImageIO_GetHighDisplayValue)
    GetLowDisplayValue = _swig_new_instance_method(_itkStimulateImageIOPython.itkStimulateImageIO_GetLowDisplayValue)
    __swig_destroy__ = _itkStimulateImageIOPython.delete_itkStimulateImageIO
    cast = _swig_new_static_method(_itkStimulateImageIOPython.itkStimulateImageIO_cast)

    def New(*args, **kargs):
        """New() -> itkStimulateImageIO

        Create a new object of the class itkStimulateImageIO and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkStimulateImageIO.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkStimulateImageIO.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkStimulateImageIO.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkStimulateImageIO in _itkStimulateImageIOPython:
_itkStimulateImageIOPython.itkStimulateImageIO_swigregister(itkStimulateImageIO)
itkStimulateImageIO___New_orig__ = _itkStimulateImageIOPython.itkStimulateImageIO___New_orig__
itkStimulateImageIO_cast = _itkStimulateImageIOPython.itkStimulateImageIO_cast

class itkStimulateImageIOFactory(ITKCommonBasePython.itkObjectFactoryBase):
    r"""Proxy of C++ itkStimulateImageIOFactory class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkStimulateImageIOPython.itkStimulateImageIOFactory___New_orig__)
    RegisterOneFactory = _swig_new_static_method(_itkStimulateImageIOPython.itkStimulateImageIOFactory_RegisterOneFactory)
    __swig_destroy__ = _itkStimulateImageIOPython.delete_itkStimulateImageIOFactory
    cast = _swig_new_static_method(_itkStimulateImageIOPython.itkStimulateImageIOFactory_cast)

    def New(*args, **kargs):
        """New() -> itkStimulateImageIOFactory

        Create a new object of the class itkStimulateImageIOFactory and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkStimulateImageIOFactory.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkStimulateImageIOFactory.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkStimulateImageIOFactory.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkStimulateImageIOFactory in _itkStimulateImageIOPython:
_itkStimulateImageIOPython.itkStimulateImageIOFactory_swigregister(itkStimulateImageIOFactory)
itkStimulateImageIOFactory___New_orig__ = _itkStimulateImageIOPython.itkStimulateImageIOFactory___New_orig__
itkStimulateImageIOFactory_RegisterOneFactory = _itkStimulateImageIOPython.itkStimulateImageIOFactory_RegisterOneFactory
itkStimulateImageIOFactory_cast = _itkStimulateImageIOPython.itkStimulateImageIOFactory_cast



