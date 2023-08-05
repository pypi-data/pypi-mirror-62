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
    from . import _itkSpatialObjectReaderPython
else:
    import _itkSpatialObjectReaderPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkSpatialObjectReaderPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkSpatialObjectReaderPython.SWIG_PyStaticMethod_New

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


import itkGroupSpatialObjectPython
import itkSpatialObjectBasePython
import itkPointPython
import itkFixedArrayPython
import pyBasePython
import itkVectorPython
import vnl_vectorPython
import vnl_matrixPython
import stdcomplexPython
import vnl_vector_refPython
import itkSpatialObjectPropertyPython
import ITKCommonBasePython
import itkRGBAPixelPython
import itkImageRegionPython
import itkSizePython
import itkIndexPython
import itkOffsetPython
import itkCovariantVectorPython
import itkAffineTransformPython
import itkTransformBasePython
import itkOptimizerParametersPython
import itkArrayPython
import vnl_matrix_fixedPython
import itkVariableLengthVectorPython
import itkDiffusionTensor3DPython
import itkSymmetricSecondRankTensorPython
import itkMatrixPython
import itkArray2DPython
import itkMatrixOffsetTransformBasePython
import itkBoundingBoxPython
import itkVectorContainerPython
import itkContinuousIndexPython
import itkMapContainerPython
import itkMetaConverterBasePython

def itkSpatialObjectReader3_New():
  return itkSpatialObjectReader3.New()


def itkSpatialObjectReader2_New():
  return itkSpatialObjectReader2.New()

class itkSpatialObjectReader2(ITKCommonBasePython.itkObject):
    r"""Proxy of C++ itkSpatialObjectReader2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2___New_orig__)
    Clone = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_Clone)
    Update = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_Update)
    SetFileName = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_SetFileName)
    GetFileName = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_GetFileName)
    GetOutput = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_GetOutput)
    GetGroup = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_GetGroup)
    GetEvent = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_GetEvent)
    SetEvent = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_SetEvent)
    RegisterMetaConverter = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_RegisterMetaConverter)
    __swig_destroy__ = _itkSpatialObjectReaderPython.delete_itkSpatialObjectReader2
    cast = _swig_new_static_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader2_cast)

    def New(*args, **kargs):
        """New() -> itkSpatialObjectReader2

        Create a new object of the class itkSpatialObjectReader2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkSpatialObjectReader2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkSpatialObjectReader2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkSpatialObjectReader2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkSpatialObjectReader2 in _itkSpatialObjectReaderPython:
_itkSpatialObjectReaderPython.itkSpatialObjectReader2_swigregister(itkSpatialObjectReader2)
itkSpatialObjectReader2___New_orig__ = _itkSpatialObjectReaderPython.itkSpatialObjectReader2___New_orig__
itkSpatialObjectReader2_cast = _itkSpatialObjectReaderPython.itkSpatialObjectReader2_cast

class itkSpatialObjectReader3(ITKCommonBasePython.itkObject):
    r"""Proxy of C++ itkSpatialObjectReader3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3___New_orig__)
    Clone = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_Clone)
    Update = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_Update)
    SetFileName = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_SetFileName)
    GetFileName = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_GetFileName)
    GetOutput = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_GetOutput)
    GetGroup = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_GetGroup)
    GetEvent = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_GetEvent)
    SetEvent = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_SetEvent)
    RegisterMetaConverter = _swig_new_instance_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_RegisterMetaConverter)
    __swig_destroy__ = _itkSpatialObjectReaderPython.delete_itkSpatialObjectReader3
    cast = _swig_new_static_method(_itkSpatialObjectReaderPython.itkSpatialObjectReader3_cast)

    def New(*args, **kargs):
        """New() -> itkSpatialObjectReader3

        Create a new object of the class itkSpatialObjectReader3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkSpatialObjectReader3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkSpatialObjectReader3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkSpatialObjectReader3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkSpatialObjectReader3 in _itkSpatialObjectReaderPython:
_itkSpatialObjectReaderPython.itkSpatialObjectReader3_swigregister(itkSpatialObjectReader3)
itkSpatialObjectReader3___New_orig__ = _itkSpatialObjectReaderPython.itkSpatialObjectReader3___New_orig__
itkSpatialObjectReader3_cast = _itkSpatialObjectReaderPython.itkSpatialObjectReader3_cast



