# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _itkBioRadImageIOPython.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_itkBioRadImageIOPython', [dirname(__file__)])
        except ImportError:
            import _itkBioRadImageIOPython
            return _itkBioRadImageIOPython
        if fp is not None:
            try:
                _mod = imp.load_module('_itkBioRadImageIOPython', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _itkBioRadImageIOPython = swig_import_helper()
    del swig_import_helper
else:
    import _itkBioRadImageIOPython
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


import ITKIOImageBaseBasePython
import vnl_vectorPython
import vnl_matrixPython
import stdcomplexPython
import pyBasePython
import ITKCommonBasePython

def itkBioRadImageIOFactory_New():
  return itkBioRadImageIOFactory.New()


def itkBioRadImageIO_New():
  return itkBioRadImageIO.New()

class itkBioRadImageIO(ITKIOImageBaseBasePython.itkImageIOBase):
    """


    ImageIO class for reading Bio-Rad images. Bio-Rad file format are used
    by confocal microscopes like MRC 1024, MRC 600http://www.bio-rad.com/.

    The reader/writer was based on a scanned copy of the MRC-600 documenta
    tionhttp://forums.ni.com/attachments/ni/200/7567/1/file%20format.pdf

    C++ includes: itkBioRadImageIO.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkBioRadImageIO_Pointer":
        """__New_orig__() -> itkBioRadImageIO_Pointer"""
        return _itkBioRadImageIOPython.itkBioRadImageIO___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkBioRadImageIO_Pointer":
        """Clone(itkBioRadImageIO self) -> itkBioRadImageIO_Pointer"""
        return _itkBioRadImageIOPython.itkBioRadImageIO_Clone(self)

    __swig_destroy__ = _itkBioRadImageIOPython.delete_itkBioRadImageIO

    def cast(obj: 'itkLightObject') -> "itkBioRadImageIO *":
        """cast(itkLightObject obj) -> itkBioRadImageIO"""
        return _itkBioRadImageIOPython.itkBioRadImageIO_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkBioRadImageIO

        Create a new object of the class itkBioRadImageIO and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBioRadImageIO.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkBioRadImageIO.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkBioRadImageIO.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkBioRadImageIO.Clone = new_instancemethod(_itkBioRadImageIOPython.itkBioRadImageIO_Clone, None, itkBioRadImageIO)
itkBioRadImageIO_swigregister = _itkBioRadImageIOPython.itkBioRadImageIO_swigregister
itkBioRadImageIO_swigregister(itkBioRadImageIO)

def itkBioRadImageIO___New_orig__() -> "itkBioRadImageIO_Pointer":
    """itkBioRadImageIO___New_orig__() -> itkBioRadImageIO_Pointer"""
    return _itkBioRadImageIOPython.itkBioRadImageIO___New_orig__()

def itkBioRadImageIO_cast(obj: 'itkLightObject') -> "itkBioRadImageIO *":
    """itkBioRadImageIO_cast(itkLightObject obj) -> itkBioRadImageIO"""
    return _itkBioRadImageIOPython.itkBioRadImageIO_cast(obj)

class itkBioRadImageIOFactory(ITKCommonBasePython.itkObjectFactoryBase):
    """


    Create instances of BioRadImageIO objects using an object factory.

    C++ includes: itkBioRadImageIOFactory.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkBioRadImageIOFactory_Pointer":
        """__New_orig__() -> itkBioRadImageIOFactory_Pointer"""
        return _itkBioRadImageIOPython.itkBioRadImageIOFactory___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def RegisterOneFactory() -> "void":
        """RegisterOneFactory()"""
        return _itkBioRadImageIOPython.itkBioRadImageIOFactory_RegisterOneFactory()

    RegisterOneFactory = staticmethod(RegisterOneFactory)
    __swig_destroy__ = _itkBioRadImageIOPython.delete_itkBioRadImageIOFactory

    def cast(obj: 'itkLightObject') -> "itkBioRadImageIOFactory *":
        """cast(itkLightObject obj) -> itkBioRadImageIOFactory"""
        return _itkBioRadImageIOPython.itkBioRadImageIOFactory_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkBioRadImageIOFactory

        Create a new object of the class itkBioRadImageIOFactory and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBioRadImageIOFactory.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkBioRadImageIOFactory.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkBioRadImageIOFactory.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkBioRadImageIOFactory_swigregister = _itkBioRadImageIOPython.itkBioRadImageIOFactory_swigregister
itkBioRadImageIOFactory_swigregister(itkBioRadImageIOFactory)

def itkBioRadImageIOFactory___New_orig__() -> "itkBioRadImageIOFactory_Pointer":
    """itkBioRadImageIOFactory___New_orig__() -> itkBioRadImageIOFactory_Pointer"""
    return _itkBioRadImageIOPython.itkBioRadImageIOFactory___New_orig__()

def itkBioRadImageIOFactory_RegisterOneFactory() -> "void":
    """itkBioRadImageIOFactory_RegisterOneFactory()"""
    return _itkBioRadImageIOPython.itkBioRadImageIOFactory_RegisterOneFactory()

def itkBioRadImageIOFactory_cast(obj: 'itkLightObject') -> "itkBioRadImageIOFactory *":
    """itkBioRadImageIOFactory_cast(itkLightObject obj) -> itkBioRadImageIOFactory"""
    return _itkBioRadImageIOPython.itkBioRadImageIOFactory_cast(obj)



