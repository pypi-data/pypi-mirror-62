# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _itkTransformFileReaderPython.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_itkTransformFileReaderPython', [dirname(__file__)])
        except ImportError:
            import _itkTransformFileReaderPython
            return _itkTransformFileReaderPython
        if fp is not None:
            try:
                _mod = imp.load_module('_itkTransformFileReaderPython', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _itkTransformFileReaderPython = swig_import_helper()
    del swig_import_helper
else:
    import _itkTransformFileReaderPython
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        object.__setattr__(self, name, value)
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0



def _swig_setattr_nondynamic_method(set):
    def set_attr(self, name, value):
        if (name == "thisown"):
            return self.this.own(value)
        if hasattr(self, name) or (name == "this"):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add attributes to %s" % self)
    return set_attr


import itkTransformIOBaseTemplatePython
import itkTransformBasePython
import itkVariableLengthVectorPython
import stdcomplexPython
import pyBasePython
import itkVectorPython
import vnl_vector_refPython
import vnl_vectorPython
import vnl_matrixPython
import itkFixedArrayPython
import itkOptimizerParametersPython
import itkArrayPython
import ITKCommonBasePython
import itkSymmetricSecondRankTensorPython
import itkMatrixPython
import vnl_matrix_fixedPython
import itkPointPython
import itkCovariantVectorPython
import itkDiffusionTensor3DPython
import itkArray2DPython

def itkTransformFileReaderTemplateF_New():
  return itkTransformFileReaderTemplateF.New()


def itkTransformFileReaderTemplateD_New():
  return itkTransformFileReaderTemplateD.New()

class itkTransformFileReaderTemplateD(ITKCommonBasePython.itkLightProcessObject):
    """Proxy of C++ itkTransformFileReaderTemplateD class."""

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkTransformFileReaderTemplateD_Pointer":
        """__New_orig__() -> itkTransformFileReaderTemplateD_Pointer"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkTransformFileReaderTemplateD_Pointer":
        """Clone(itkTransformFileReaderTemplateD self) -> itkTransformFileReaderTemplateD_Pointer"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_Clone(self)


    def SetFileName(self, *args) -> "void":
        """
        SetFileName(itkTransformFileReaderTemplateD self, char const * _arg)
        SetFileName(itkTransformFileReaderTemplateD self, std::string const & _arg)
        """
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_SetFileName(self, *args)


    def GetFileName(self) -> "char const *":
        """GetFileName(itkTransformFileReaderTemplateD self) -> char const *"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_GetFileName(self)


    def Update(self) -> "void":
        """Update(itkTransformFileReaderTemplateD self)"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_Update(self)


    def GetTransformList(self) -> "std::list< itkTransformBaseTemplateD_Pointer,std::allocator< itkTransformBaseTemplateD_Pointer > > const *":
        """GetTransformList(itkTransformFileReaderTemplateD self) -> listitkTransformBaseTemplateD_Pointer"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_GetTransformList(self)


    def GetModifiableTransformList(self) -> "std::list< itkTransformBaseTemplateD_Pointer,std::allocator< itkTransformBaseTemplateD_Pointer > > *":
        """GetModifiableTransformList(itkTransformFileReaderTemplateD self) -> listitkTransformBaseTemplateD_Pointer"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_GetModifiableTransformList(self)


    def SetTransformIO(self, _arg: 'itkTransformIOBaseTemplateD') -> "void":
        """SetTransformIO(itkTransformFileReaderTemplateD self, itkTransformIOBaseTemplateD _arg)"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_SetTransformIO(self, _arg)


    def GetTransformIO(self) -> "itkTransformIOBaseTemplateD const *":
        """GetTransformIO(itkTransformFileReaderTemplateD self) -> itkTransformIOBaseTemplateD"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_GetTransformIO(self)

    __swig_destroy__ = _itkTransformFileReaderPython.delete_itkTransformFileReaderTemplateD

    def cast(obj: 'itkLightObject') -> "itkTransformFileReaderTemplateD *":
        """cast(itkLightObject obj) -> itkTransformFileReaderTemplateD"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkTransformFileReaderTemplateD

        Create a new object of the class itkTransformFileReaderTemplateD and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformFileReaderTemplateD.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformFileReaderTemplateD.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformFileReaderTemplateD.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkTransformFileReaderTemplateD.Clone = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateD_Clone, None, itkTransformFileReaderTemplateD)
itkTransformFileReaderTemplateD.SetFileName = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateD_SetFileName, None, itkTransformFileReaderTemplateD)
itkTransformFileReaderTemplateD.GetFileName = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateD_GetFileName, None, itkTransformFileReaderTemplateD)
itkTransformFileReaderTemplateD.Update = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateD_Update, None, itkTransformFileReaderTemplateD)
itkTransformFileReaderTemplateD.GetTransformList = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateD_GetTransformList, None, itkTransformFileReaderTemplateD)
itkTransformFileReaderTemplateD.GetModifiableTransformList = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateD_GetModifiableTransformList, None, itkTransformFileReaderTemplateD)
itkTransformFileReaderTemplateD.SetTransformIO = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateD_SetTransformIO, None, itkTransformFileReaderTemplateD)
itkTransformFileReaderTemplateD.GetTransformIO = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateD_GetTransformIO, None, itkTransformFileReaderTemplateD)
itkTransformFileReaderTemplateD_swigregister = _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_swigregister
itkTransformFileReaderTemplateD_swigregister(itkTransformFileReaderTemplateD)

def itkTransformFileReaderTemplateD___New_orig__() -> "itkTransformFileReaderTemplateD_Pointer":
    """itkTransformFileReaderTemplateD___New_orig__() -> itkTransformFileReaderTemplateD_Pointer"""
    return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD___New_orig__()

def itkTransformFileReaderTemplateD_cast(obj: 'itkLightObject') -> "itkTransformFileReaderTemplateD *":
    """itkTransformFileReaderTemplateD_cast(itkLightObject obj) -> itkTransformFileReaderTemplateD"""
    return _itkTransformFileReaderPython.itkTransformFileReaderTemplateD_cast(obj)

class itkTransformFileReaderTemplateF(ITKCommonBasePython.itkLightProcessObject):
    """Proxy of C++ itkTransformFileReaderTemplateF class."""

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkTransformFileReaderTemplateF_Pointer":
        """__New_orig__() -> itkTransformFileReaderTemplateF_Pointer"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkTransformFileReaderTemplateF_Pointer":
        """Clone(itkTransformFileReaderTemplateF self) -> itkTransformFileReaderTemplateF_Pointer"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_Clone(self)


    def SetFileName(self, *args) -> "void":
        """
        SetFileName(itkTransformFileReaderTemplateF self, char const * _arg)
        SetFileName(itkTransformFileReaderTemplateF self, std::string const & _arg)
        """
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_SetFileName(self, *args)


    def GetFileName(self) -> "char const *":
        """GetFileName(itkTransformFileReaderTemplateF self) -> char const *"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_GetFileName(self)


    def Update(self) -> "void":
        """Update(itkTransformFileReaderTemplateF self)"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_Update(self)


    def GetTransformList(self) -> "std::list< itkTransformBaseTemplateF_Pointer,std::allocator< itkTransformBaseTemplateF_Pointer > > const *":
        """GetTransformList(itkTransformFileReaderTemplateF self) -> listitkTransformBaseTemplateF_Pointer"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_GetTransformList(self)


    def GetModifiableTransformList(self) -> "std::list< itkTransformBaseTemplateF_Pointer,std::allocator< itkTransformBaseTemplateF_Pointer > > *":
        """GetModifiableTransformList(itkTransformFileReaderTemplateF self) -> listitkTransformBaseTemplateF_Pointer"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_GetModifiableTransformList(self)


    def SetTransformIO(self, _arg: 'itkTransformIOBaseTemplateF') -> "void":
        """SetTransformIO(itkTransformFileReaderTemplateF self, itkTransformIOBaseTemplateF _arg)"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_SetTransformIO(self, _arg)


    def GetTransformIO(self) -> "itkTransformIOBaseTemplateF const *":
        """GetTransformIO(itkTransformFileReaderTemplateF self) -> itkTransformIOBaseTemplateF"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_GetTransformIO(self)

    __swig_destroy__ = _itkTransformFileReaderPython.delete_itkTransformFileReaderTemplateF

    def cast(obj: 'itkLightObject') -> "itkTransformFileReaderTemplateF *":
        """cast(itkLightObject obj) -> itkTransformFileReaderTemplateF"""
        return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkTransformFileReaderTemplateF

        Create a new object of the class itkTransformFileReaderTemplateF and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformFileReaderTemplateF.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformFileReaderTemplateF.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformFileReaderTemplateF.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkTransformFileReaderTemplateF.Clone = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateF_Clone, None, itkTransformFileReaderTemplateF)
itkTransformFileReaderTemplateF.SetFileName = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateF_SetFileName, None, itkTransformFileReaderTemplateF)
itkTransformFileReaderTemplateF.GetFileName = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateF_GetFileName, None, itkTransformFileReaderTemplateF)
itkTransformFileReaderTemplateF.Update = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateF_Update, None, itkTransformFileReaderTemplateF)
itkTransformFileReaderTemplateF.GetTransformList = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateF_GetTransformList, None, itkTransformFileReaderTemplateF)
itkTransformFileReaderTemplateF.GetModifiableTransformList = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateF_GetModifiableTransformList, None, itkTransformFileReaderTemplateF)
itkTransformFileReaderTemplateF.SetTransformIO = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateF_SetTransformIO, None, itkTransformFileReaderTemplateF)
itkTransformFileReaderTemplateF.GetTransformIO = new_instancemethod(_itkTransformFileReaderPython.itkTransformFileReaderTemplateF_GetTransformIO, None, itkTransformFileReaderTemplateF)
itkTransformFileReaderTemplateF_swigregister = _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_swigregister
itkTransformFileReaderTemplateF_swigregister(itkTransformFileReaderTemplateF)

def itkTransformFileReaderTemplateF___New_orig__() -> "itkTransformFileReaderTemplateF_Pointer":
    """itkTransformFileReaderTemplateF___New_orig__() -> itkTransformFileReaderTemplateF_Pointer"""
    return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF___New_orig__()

def itkTransformFileReaderTemplateF_cast(obj: 'itkLightObject') -> "itkTransformFileReaderTemplateF *":
    """itkTransformFileReaderTemplateF_cast(itkLightObject obj) -> itkTransformFileReaderTemplateF"""
    return _itkTransformFileReaderPython.itkTransformFileReaderTemplateF_cast(obj)



