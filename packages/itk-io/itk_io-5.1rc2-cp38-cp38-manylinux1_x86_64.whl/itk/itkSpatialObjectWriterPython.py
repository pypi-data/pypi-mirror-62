# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _itkSpatialObjectWriterPython.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_itkSpatialObjectWriterPython', [dirname(__file__)])
        except ImportError:
            import _itkSpatialObjectWriterPython
            return _itkSpatialObjectWriterPython
        if fp is not None:
            try:
                _mod = imp.load_module('_itkSpatialObjectWriterPython', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _itkSpatialObjectWriterPython = swig_import_helper()
    del swig_import_helper
else:
    import _itkSpatialObjectWriterPython
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


import itkMetaConverterBasePython
import ITKCommonBasePython
import pyBasePython
import itkSpatialObjectBasePython
import itkPointPython
import vnl_vector_refPython
import vnl_vectorPython
import stdcomplexPython
import vnl_matrixPython
import itkVectorPython
import itkFixedArrayPython
import itkImageRegionPython
import itkIndexPython
import itkSizePython
import itkOffsetPython
import itkSpatialObjectPropertyPython
import itkRGBAPixelPython
import itkAffineTransformPython
import itkMatrixOffsetTransformBasePython
import itkOptimizerParametersPython
import itkArrayPython
import vnl_matrix_fixedPython
import itkVariableLengthVectorPython
import itkArray2DPython
import itkDiffusionTensor3DPython
import itkSymmetricSecondRankTensorPython
import itkMatrixPython
import itkCovariantVectorPython
import itkTransformBasePython
import itkBoundingBoxPython
import itkMapContainerPython
import itkVectorContainerPython
import itkContinuousIndexPython

def itkSpatialObjectWriter3_New():
  return itkSpatialObjectWriter3.New()


def itkSpatialObjectWriter2_New():
  return itkSpatialObjectWriter2.New()

class itkSpatialObjectWriter2(ITKCommonBasePython.itkObject):
    """


    TODO.

    C++ includes: itkSpatialObjectWriter.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkSpatialObjectWriter2_Pointer":
        """__New_orig__() -> itkSpatialObjectWriter2_Pointer"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkSpatialObjectWriter2_Pointer":
        """Clone(itkSpatialObjectWriter2 self) -> itkSpatialObjectWriter2_Pointer"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_Clone(self)


    def Update(self) -> "void":
        """
        Update(itkSpatialObjectWriter2 self)

        Load a tube file. 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_Update(self)


    def SetFileName(self, *args) -> "void":
        """
        SetFileName(itkSpatialObjectWriter2 self, char const * _arg)
        SetFileName(itkSpatialObjectWriter2 self, std::string const & _arg)

        Set the filename 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetFileName(self, *args)


    def GetFileName(self) -> "char const *":
        """
        GetFileName(itkSpatialObjectWriter2 self) -> char const *

        Get the filename 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_GetFileName(self)


    def SetInput(self, input: 'itkSpatialObject2') -> "void":
        """
        SetInput(itkSpatialObjectWriter2 self, itkSpatialObject2 input)

        Set the Input 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetInput(self, input)


    def SetBinaryPoints(self, _arg: 'bool const') -> "void":
        """SetBinaryPoints(itkSpatialObjectWriter2 self, bool const _arg)"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetBinaryPoints(self, _arg)


    def GetBinaryPoints(self) -> "bool":
        """GetBinaryPoints(itkSpatialObjectWriter2 self) -> bool"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_GetBinaryPoints(self)


    def SetTransformPrecision(self, precision: 'unsigned int') -> "void":
        """SetTransformPrecision(itkSpatialObjectWriter2 self, unsigned int precision)"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetTransformPrecision(self, precision)


    def GetTransformPrecision(self) -> "unsigned int":
        """GetTransformPrecision(itkSpatialObjectWriter2 self) -> unsigned int"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_GetTransformPrecision(self)


    def SetWriteImagesInSeparateFile(self, _arg: 'bool const') -> "void":
        """
        SetWriteImagesInSeparateFile(itkSpatialObjectWriter2 self, bool const _arg)

        Set/Get if the images should be written in a different file 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetWriteImagesInSeparateFile(self, _arg)


    def GetWriteImagesInSeparateFile(self) -> "bool":
        """GetWriteImagesInSeparateFile(itkSpatialObjectWriter2 self) -> bool"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_GetWriteImagesInSeparateFile(self)


    def RegisterMetaConverter(self, metaTypeName: 'char const *', spatialObjectTypeName: 'char const *', converter: 'itkMetaConverterBase2') -> "void":
        """
        RegisterMetaConverter(itkSpatialObjectWriter2 self, char const * metaTypeName, char const * spatialObjectTypeName, itkMetaConverterBase2 converter)

        Add a
        converter for a new MetaObject/SpatialObject type 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_RegisterMetaConverter(self, metaTypeName, spatialObjectTypeName, converter)

    __swig_destroy__ = _itkSpatialObjectWriterPython.delete_itkSpatialObjectWriter2

    def cast(obj: 'itkLightObject') -> "itkSpatialObjectWriter2 *":
        """cast(itkLightObject obj) -> itkSpatialObjectWriter2"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkSpatialObjectWriter2

        Create a new object of the class itkSpatialObjectWriter2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkSpatialObjectWriter2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkSpatialObjectWriter2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkSpatialObjectWriter2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkSpatialObjectWriter2.Clone = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_Clone, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.Update = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_Update, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.SetFileName = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetFileName, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.GetFileName = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_GetFileName, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.SetInput = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetInput, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.SetBinaryPoints = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetBinaryPoints, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.GetBinaryPoints = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_GetBinaryPoints, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.SetTransformPrecision = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetTransformPrecision, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.GetTransformPrecision = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_GetTransformPrecision, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.SetWriteImagesInSeparateFile = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_SetWriteImagesInSeparateFile, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.GetWriteImagesInSeparateFile = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_GetWriteImagesInSeparateFile, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2.RegisterMetaConverter = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter2_RegisterMetaConverter, None, itkSpatialObjectWriter2)
itkSpatialObjectWriter2_swigregister = _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_swigregister
itkSpatialObjectWriter2_swigregister(itkSpatialObjectWriter2)

def itkSpatialObjectWriter2___New_orig__() -> "itkSpatialObjectWriter2_Pointer":
    """itkSpatialObjectWriter2___New_orig__() -> itkSpatialObjectWriter2_Pointer"""
    return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2___New_orig__()

def itkSpatialObjectWriter2_cast(obj: 'itkLightObject') -> "itkSpatialObjectWriter2 *":
    """itkSpatialObjectWriter2_cast(itkLightObject obj) -> itkSpatialObjectWriter2"""
    return _itkSpatialObjectWriterPython.itkSpatialObjectWriter2_cast(obj)

class itkSpatialObjectWriter3(ITKCommonBasePython.itkObject):
    """


    TODO.

    C++ includes: itkSpatialObjectWriter.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkSpatialObjectWriter3_Pointer":
        """__New_orig__() -> itkSpatialObjectWriter3_Pointer"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkSpatialObjectWriter3_Pointer":
        """Clone(itkSpatialObjectWriter3 self) -> itkSpatialObjectWriter3_Pointer"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_Clone(self)


    def Update(self) -> "void":
        """
        Update(itkSpatialObjectWriter3 self)

        Load a tube file. 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_Update(self)


    def SetFileName(self, *args) -> "void":
        """
        SetFileName(itkSpatialObjectWriter3 self, char const * _arg)
        SetFileName(itkSpatialObjectWriter3 self, std::string const & _arg)

        Set the filename 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetFileName(self, *args)


    def GetFileName(self) -> "char const *":
        """
        GetFileName(itkSpatialObjectWriter3 self) -> char const *

        Get the filename 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_GetFileName(self)


    def SetInput(self, input: 'itkSpatialObject3') -> "void":
        """
        SetInput(itkSpatialObjectWriter3 self, itkSpatialObject3 input)

        Set the Input 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetInput(self, input)


    def SetBinaryPoints(self, _arg: 'bool const') -> "void":
        """SetBinaryPoints(itkSpatialObjectWriter3 self, bool const _arg)"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetBinaryPoints(self, _arg)


    def GetBinaryPoints(self) -> "bool":
        """GetBinaryPoints(itkSpatialObjectWriter3 self) -> bool"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_GetBinaryPoints(self)


    def SetTransformPrecision(self, precision: 'unsigned int') -> "void":
        """SetTransformPrecision(itkSpatialObjectWriter3 self, unsigned int precision)"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetTransformPrecision(self, precision)


    def GetTransformPrecision(self) -> "unsigned int":
        """GetTransformPrecision(itkSpatialObjectWriter3 self) -> unsigned int"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_GetTransformPrecision(self)


    def SetWriteImagesInSeparateFile(self, _arg: 'bool const') -> "void":
        """
        SetWriteImagesInSeparateFile(itkSpatialObjectWriter3 self, bool const _arg)

        Set/Get if the images should be written in a different file 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetWriteImagesInSeparateFile(self, _arg)


    def GetWriteImagesInSeparateFile(self) -> "bool":
        """GetWriteImagesInSeparateFile(itkSpatialObjectWriter3 self) -> bool"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_GetWriteImagesInSeparateFile(self)


    def RegisterMetaConverter(self, metaTypeName: 'char const *', spatialObjectTypeName: 'char const *', converter: 'itkMetaConverterBase3') -> "void":
        """
        RegisterMetaConverter(itkSpatialObjectWriter3 self, char const * metaTypeName, char const * spatialObjectTypeName, itkMetaConverterBase3 converter)

        Add a
        converter for a new MetaObject/SpatialObject type 
        """
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_RegisterMetaConverter(self, metaTypeName, spatialObjectTypeName, converter)

    __swig_destroy__ = _itkSpatialObjectWriterPython.delete_itkSpatialObjectWriter3

    def cast(obj: 'itkLightObject') -> "itkSpatialObjectWriter3 *":
        """cast(itkLightObject obj) -> itkSpatialObjectWriter3"""
        return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkSpatialObjectWriter3

        Create a new object of the class itkSpatialObjectWriter3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkSpatialObjectWriter3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkSpatialObjectWriter3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkSpatialObjectWriter3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkSpatialObjectWriter3.Clone = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_Clone, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.Update = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_Update, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.SetFileName = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetFileName, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.GetFileName = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_GetFileName, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.SetInput = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetInput, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.SetBinaryPoints = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetBinaryPoints, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.GetBinaryPoints = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_GetBinaryPoints, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.SetTransformPrecision = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetTransformPrecision, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.GetTransformPrecision = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_GetTransformPrecision, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.SetWriteImagesInSeparateFile = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_SetWriteImagesInSeparateFile, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.GetWriteImagesInSeparateFile = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_GetWriteImagesInSeparateFile, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3.RegisterMetaConverter = new_instancemethod(_itkSpatialObjectWriterPython.itkSpatialObjectWriter3_RegisterMetaConverter, None, itkSpatialObjectWriter3)
itkSpatialObjectWriter3_swigregister = _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_swigregister
itkSpatialObjectWriter3_swigregister(itkSpatialObjectWriter3)

def itkSpatialObjectWriter3___New_orig__() -> "itkSpatialObjectWriter3_Pointer":
    """itkSpatialObjectWriter3___New_orig__() -> itkSpatialObjectWriter3_Pointer"""
    return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3___New_orig__()

def itkSpatialObjectWriter3_cast(obj: 'itkLightObject') -> "itkSpatialObjectWriter3 *":
    """itkSpatialObjectWriter3_cast(itkLightObject obj) -> itkSpatialObjectWriter3"""
    return _itkSpatialObjectWriterPython.itkSpatialObjectWriter3_cast(obj)



