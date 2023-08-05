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
    from . import _itkTransformIOBaseTemplatePython
else:
    import _itkTransformIOBaseTemplatePython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkTransformIOBaseTemplatePython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkTransformIOBaseTemplatePython.SWIG_PyStaticMethod_New

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
import itkDiffusionTensor3DPython
import itkSymmetricSecondRankTensorPython
import itkMatrixPython
import itkPointPython
import vnl_vectorPython
import vnl_matrixPython
import stdcomplexPython
import vnl_vector_refPython
import itkFixedArrayPython
import itkVectorPython
import itkCovariantVectorPython
import vnl_matrix_fixedPython
import itkArray2DPython
import itkVariableLengthVectorPython
import itkOptimizerParametersPython
import itkArrayPython

def itkTransformIOBaseTemplateF_New():
  return itkTransformIOBaseTemplateF.New()


def itkTransformIOBaseTemplateD_New():
  return itkTransformIOBaseTemplateD.New()

class itkTransformIOBaseTemplateD(ITKCommonBasePython.itkLightProcessObject):
    r"""Proxy of C++ itkTransformIOBaseTemplateD class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    SetFileName = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_SetFileName)
    GetFileName = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_GetFileName)
    Read = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_Read)
    Write = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_Write)
    CanReadFile = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_CanReadFile)
    CanWriteFile = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_CanWriteFile)
    GetTransformList = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_GetTransformList)
    GetReadTransformList = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_GetReadTransformList)
    GetWriteTransformList = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_GetWriteTransformList)
    SetTransformList = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_SetTransformList)
    SetAppendMode = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_SetAppendMode)
    GetAppendMode = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_GetAppendMode)
    AppendModeOn = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_AppendModeOn)
    AppendModeOff = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_AppendModeOff)
    SetUseCompression = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_SetUseCompression)
    GetUseCompression = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_GetUseCompression)
    UseCompressionOn = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_UseCompressionOn)
    UseCompressionOff = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_UseCompressionOff)
    CorrectTransformPrecisionType = _swig_new_static_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_CorrectTransformPrecisionType)
    __swig_destroy__ = _itkTransformIOBaseTemplatePython.delete_itkTransformIOBaseTemplateD
    cast = _swig_new_static_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_cast)

    def New(*args, **kargs):
        """New() -> itkTransformIOBaseTemplateD

        Create a new object of the class itkTransformIOBaseTemplateD and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformIOBaseTemplateD.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformIOBaseTemplateD.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformIOBaseTemplateD.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkTransformIOBaseTemplateD in _itkTransformIOBaseTemplatePython:
_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_swigregister(itkTransformIOBaseTemplateD)
itkTransformIOBaseTemplateD_CorrectTransformPrecisionType = _itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_CorrectTransformPrecisionType
itkTransformIOBaseTemplateD_cast = _itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateD_cast

class itkTransformIOBaseTemplateF(ITKCommonBasePython.itkLightProcessObject):
    r"""Proxy of C++ itkTransformIOBaseTemplateF class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    SetFileName = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_SetFileName)
    GetFileName = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_GetFileName)
    Read = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_Read)
    Write = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_Write)
    CanReadFile = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_CanReadFile)
    CanWriteFile = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_CanWriteFile)
    GetTransformList = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_GetTransformList)
    GetReadTransformList = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_GetReadTransformList)
    GetWriteTransformList = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_GetWriteTransformList)
    SetTransformList = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_SetTransformList)
    SetAppendMode = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_SetAppendMode)
    GetAppendMode = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_GetAppendMode)
    AppendModeOn = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_AppendModeOn)
    AppendModeOff = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_AppendModeOff)
    SetUseCompression = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_SetUseCompression)
    GetUseCompression = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_GetUseCompression)
    UseCompressionOn = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_UseCompressionOn)
    UseCompressionOff = _swig_new_instance_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_UseCompressionOff)
    CorrectTransformPrecisionType = _swig_new_static_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_CorrectTransformPrecisionType)
    __swig_destroy__ = _itkTransformIOBaseTemplatePython.delete_itkTransformIOBaseTemplateF
    cast = _swig_new_static_method(_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_cast)

    def New(*args, **kargs):
        """New() -> itkTransformIOBaseTemplateF

        Create a new object of the class itkTransformIOBaseTemplateF and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformIOBaseTemplateF.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformIOBaseTemplateF.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformIOBaseTemplateF.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkTransformIOBaseTemplateF in _itkTransformIOBaseTemplatePython:
_itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_swigregister(itkTransformIOBaseTemplateF)
itkTransformIOBaseTemplateF_CorrectTransformPrecisionType = _itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_CorrectTransformPrecisionType
itkTransformIOBaseTemplateF_cast = _itkTransformIOBaseTemplatePython.itkTransformIOBaseTemplateF_cast



