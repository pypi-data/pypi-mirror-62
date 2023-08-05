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
    from . import _itkTransformFileWriterPython
else:
    import _itkTransformFileWriterPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkTransformFileWriterPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkTransformFileWriterPython.SWIG_PyStaticMethod_New

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
import itkTransformBasePython
import itkPointPython
import vnl_vector_refPython
import vnl_vectorPython
import vnl_matrixPython
import stdcomplexPython
import itkFixedArrayPython
import itkVectorPython
import itkCovariantVectorPython
import itkSymmetricSecondRankTensorPython
import itkMatrixPython
import vnl_matrix_fixedPython
import itkOptimizerParametersPython
import itkArrayPython
import itkArray2DPython
import itkVariableLengthVectorPython
import itkDiffusionTensor3DPython
import itkTransformIOBaseTemplatePython

def itkTransformFileWriterTemplateD_New():
  return itkTransformFileWriterTemplateD.New()


def itkTransformFileWriterTemplateF_New():
  return itkTransformFileWriterTemplateF.New()

class itkTransformFileWriterTemplateD(ITKCommonBasePython.itkLightProcessObject):
    r"""Proxy of C++ itkTransformFileWriterTemplateD class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD___New_orig__)
    Clone = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_Clone)
    SetFileName = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_SetFileName)
    GetFileName = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_GetFileName)
    SetAppendOff = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_SetAppendOff)
    SetAppendOn = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_SetAppendOn)
    SetAppendMode = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_SetAppendMode)
    GetAppendMode = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_GetAppendMode)
    SetUseCompression = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_SetUseCompression)
    GetUseCompression = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_GetUseCompression)
    UseCompressionOn = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_UseCompressionOn)
    UseCompressionOff = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_UseCompressionOff)
    SetInput = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_SetInput)
    GetInput = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_GetInput)
    AddTransform = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_AddTransform)
    Update = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_Update)
    SetTransformIO = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_SetTransformIO)
    GetTransformIO = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_GetTransformIO)
    __swig_destroy__ = _itkTransformFileWriterPython.delete_itkTransformFileWriterTemplateD
    cast = _swig_new_static_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_cast)

    def New(*args, **kargs):
        """New() -> itkTransformFileWriterTemplateD

        Create a new object of the class itkTransformFileWriterTemplateD and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformFileWriterTemplateD.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformFileWriterTemplateD.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformFileWriterTemplateD.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkTransformFileWriterTemplateD in _itkTransformFileWriterPython:
_itkTransformFileWriterPython.itkTransformFileWriterTemplateD_swigregister(itkTransformFileWriterTemplateD)
itkTransformFileWriterTemplateD___New_orig__ = _itkTransformFileWriterPython.itkTransformFileWriterTemplateD___New_orig__
itkTransformFileWriterTemplateD_cast = _itkTransformFileWriterPython.itkTransformFileWriterTemplateD_cast

class itkTransformFileWriterTemplateF(ITKCommonBasePython.itkLightProcessObject):
    r"""Proxy of C++ itkTransformFileWriterTemplateF class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF___New_orig__)
    Clone = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_Clone)
    SetFileName = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_SetFileName)
    GetFileName = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_GetFileName)
    SetAppendOff = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_SetAppendOff)
    SetAppendOn = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_SetAppendOn)
    SetAppendMode = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_SetAppendMode)
    GetAppendMode = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_GetAppendMode)
    SetUseCompression = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_SetUseCompression)
    GetUseCompression = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_GetUseCompression)
    UseCompressionOn = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_UseCompressionOn)
    UseCompressionOff = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_UseCompressionOff)
    SetInput = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_SetInput)
    GetInput = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_GetInput)
    AddTransform = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_AddTransform)
    Update = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_Update)
    SetTransformIO = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_SetTransformIO)
    GetTransformIO = _swig_new_instance_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_GetTransformIO)
    __swig_destroy__ = _itkTransformFileWriterPython.delete_itkTransformFileWriterTemplateF
    cast = _swig_new_static_method(_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_cast)

    def New(*args, **kargs):
        """New() -> itkTransformFileWriterTemplateF

        Create a new object of the class itkTransformFileWriterTemplateF and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformFileWriterTemplateF.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformFileWriterTemplateF.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformFileWriterTemplateF.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkTransformFileWriterTemplateF in _itkTransformFileWriterPython:
_itkTransformFileWriterPython.itkTransformFileWriterTemplateF_swigregister(itkTransformFileWriterTemplateF)
itkTransformFileWriterTemplateF___New_orig__ = _itkTransformFileWriterPython.itkTransformFileWriterTemplateF___New_orig__
itkTransformFileWriterTemplateF_cast = _itkTransformFileWriterPython.itkTransformFileWriterTemplateF_cast



