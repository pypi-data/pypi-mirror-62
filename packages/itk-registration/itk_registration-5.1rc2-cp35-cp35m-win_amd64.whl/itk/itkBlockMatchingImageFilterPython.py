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
    from . import _itkBlockMatchingImageFilterPython
else:
    import _itkBlockMatchingImageFilterPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkBlockMatchingImageFilterPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkBlockMatchingImageFilterPython.SWIG_PyStaticMethod_New

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


import itkImagePython
import itkSizePython
import pyBasePython
import itkSymmetricSecondRankTensorPython
import itkFixedArrayPython
import itkMatrixPython
import vnl_matrixPython
import vnl_vectorPython
import stdcomplexPython
import vnl_matrix_fixedPython
import itkVectorPython
import vnl_vector_refPython
import itkCovariantVectorPython
import itkPointPython
import itkRGBPixelPython
import ITKCommonBasePython
import itkRGBAPixelPython
import itkOffsetPython
import itkImageRegionPython
import itkIndexPython
import itkPointSetPython
import itkVectorContainerPython
import itkContinuousIndexPython

def itkPointSetD3DTD33FFD_New():
  return itkPointSetD3DTD33FFD.New()


def itkPointSetVF33DTVF333FFVF3_New():
  return itkPointSetVF33DTVF333FFVF3.New()


def itkBlockMatchingImageFilterID3_New():
  return itkBlockMatchingImageFilterID3.New()


def itkBlockMatchingImageFilterID3_Superclass_New():
  return itkBlockMatchingImageFilterID3_Superclass.New()


def itkBlockMatchingImageFilterID3_Superclass_Superclass_New():
  return itkBlockMatchingImageFilterID3_Superclass_Superclass.New()


def itkBlockMatchingImageFilterIF3_New():
  return itkBlockMatchingImageFilterIF3.New()


def itkBlockMatchingImageFilterIF3_Superclass_New():
  return itkBlockMatchingImageFilterIF3_Superclass.New()


def itkBlockMatchingImageFilterIF3_Superclass_Superclass_New():
  return itkBlockMatchingImageFilterIF3_Superclass_Superclass.New()

class itkBlockMatchingImageFilterID3_Superclass_Superclass(ITKCommonBasePython.itkProcessObject):
    r"""Proxy of C++ itkBlockMatchingImageFilterID3_Superclass_Superclass class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass___New_orig__)
    Clone = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass_Clone)
    GetOutput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass_GetOutput)
    SetOutput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass_SetOutput)
    GraftOutput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass_GraftOutput)
    GraftNthOutput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass_GraftNthOutput)
    __swig_destroy__ = _itkBlockMatchingImageFilterPython.delete_itkBlockMatchingImageFilterID3_Superclass_Superclass
    cast = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass_cast)

    def New(*args, **kargs):
        """New() -> itkBlockMatchingImageFilterID3_Superclass_Superclass

        Create a new object of the class itkBlockMatchingImageFilterID3_Superclass_Superclass and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBlockMatchingImageFilterID3_Superclass_Superclass.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkBlockMatchingImageFilterID3_Superclass_Superclass.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkBlockMatchingImageFilterID3_Superclass_Superclass.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBlockMatchingImageFilterID3_Superclass_Superclass in _itkBlockMatchingImageFilterPython:
_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass_swigregister(itkBlockMatchingImageFilterID3_Superclass_Superclass)
itkBlockMatchingImageFilterID3_Superclass_Superclass___New_orig__ = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass___New_orig__
itkBlockMatchingImageFilterID3_Superclass_Superclass_cast = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Superclass_cast

class itkBlockMatchingImageFilterIF3_Superclass_Superclass(ITKCommonBasePython.itkProcessObject):
    r"""Proxy of C++ itkBlockMatchingImageFilterIF3_Superclass_Superclass class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass___New_orig__)
    Clone = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass_Clone)
    GetOutput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass_GetOutput)
    SetOutput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass_SetOutput)
    GraftOutput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass_GraftOutput)
    GraftNthOutput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass_GraftNthOutput)
    __swig_destroy__ = _itkBlockMatchingImageFilterPython.delete_itkBlockMatchingImageFilterIF3_Superclass_Superclass
    cast = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass_cast)

    def New(*args, **kargs):
        """New() -> itkBlockMatchingImageFilterIF3_Superclass_Superclass

        Create a new object of the class itkBlockMatchingImageFilterIF3_Superclass_Superclass and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBlockMatchingImageFilterIF3_Superclass_Superclass.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkBlockMatchingImageFilterIF3_Superclass_Superclass.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkBlockMatchingImageFilterIF3_Superclass_Superclass.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBlockMatchingImageFilterIF3_Superclass_Superclass in _itkBlockMatchingImageFilterPython:
_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass_swigregister(itkBlockMatchingImageFilterIF3_Superclass_Superclass)
itkBlockMatchingImageFilterIF3_Superclass_Superclass___New_orig__ = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass___New_orig__
itkBlockMatchingImageFilterIF3_Superclass_Superclass_cast = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Superclass_cast

class itkPointSetD3DTD33FFD(ITKCommonBasePython.itkDataObject):
    r"""Proxy of C++ itkPointSetD3DTD33FFD class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD___New_orig__)
    Clone = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_Clone)
    GetMaximumNumberOfRegions = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_GetMaximumNumberOfRegions)
    PassStructure = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_PassStructure)
    GetNumberOfPoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_GetNumberOfPoints)
    SetPoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_SetPoints)
    GetPoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_GetPoints)
    SetPoint = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_SetPoint)
    GetPoint = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_GetPoint)
    SetPointData = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_SetPointData)
    GetPointData = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_GetPointData)
    SetRequestedRegion = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_SetRequestedRegion)
    GetRequestedRegion = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_GetRequestedRegion)
    SetBufferedRegion = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_SetBufferedRegion)
    GetBufferedRegion = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_GetBufferedRegion)
    __swig_destroy__ = _itkBlockMatchingImageFilterPython.delete_itkPointSetD3DTD33FFD
    cast = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_cast)

    def New(*args, **kargs):
        """New() -> itkPointSetD3DTD33FFD

        Create a new object of the class itkPointSetD3DTD33FFD and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkPointSetD3DTD33FFD.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkPointSetD3DTD33FFD.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkPointSetD3DTD33FFD.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkPointSetD3DTD33FFD in _itkBlockMatchingImageFilterPython:
_itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_swigregister(itkPointSetD3DTD33FFD)
itkPointSetD3DTD33FFD___New_orig__ = _itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD___New_orig__
itkPointSetD3DTD33FFD_cast = _itkBlockMatchingImageFilterPython.itkPointSetD3DTD33FFD_cast

class itkPointSetVF33DTVF333FFVF3(ITKCommonBasePython.itkDataObject):
    r"""Proxy of C++ itkPointSetVF33DTVF333FFVF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3___New_orig__)
    Clone = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_Clone)
    GetMaximumNumberOfRegions = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_GetMaximumNumberOfRegions)
    PassStructure = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_PassStructure)
    GetNumberOfPoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_GetNumberOfPoints)
    SetPoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_SetPoints)
    GetPoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_GetPoints)
    SetPoint = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_SetPoint)
    GetPoint = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_GetPoint)
    SetPointData = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_SetPointData)
    GetPointData = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_GetPointData)
    SetRequestedRegion = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_SetRequestedRegion)
    GetRequestedRegion = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_GetRequestedRegion)
    SetBufferedRegion = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_SetBufferedRegion)
    GetBufferedRegion = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_GetBufferedRegion)
    __swig_destroy__ = _itkBlockMatchingImageFilterPython.delete_itkPointSetVF33DTVF333FFVF3
    cast = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_cast)

    def New(*args, **kargs):
        """New() -> itkPointSetVF33DTVF333FFVF3

        Create a new object of the class itkPointSetVF33DTVF333FFVF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkPointSetVF33DTVF333FFVF3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkPointSetVF33DTVF333FFVF3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkPointSetVF33DTVF333FFVF3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkPointSetVF33DTVF333FFVF3 in _itkBlockMatchingImageFilterPython:
_itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_swigregister(itkPointSetVF33DTVF333FFVF3)
itkPointSetVF33DTVF333FFVF3___New_orig__ = _itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3___New_orig__
itkPointSetVF33DTVF333FFVF3_cast = _itkBlockMatchingImageFilterPython.itkPointSetVF33DTVF333FFVF3_cast

class itkBlockMatchingImageFilterID3_Superclass(itkBlockMatchingImageFilterIF3_Superclass_Superclass):
    r"""Proxy of C++ itkBlockMatchingImageFilterID3_Superclass class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass___New_orig__)
    Clone = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_Clone)
    SetInput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_SetInput)
    GetInput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_GetInput)
    __swig_destroy__ = _itkBlockMatchingImageFilterPython.delete_itkBlockMatchingImageFilterID3_Superclass
    cast = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_cast)

    def New(*args, **kargs):
        """New() -> itkBlockMatchingImageFilterID3_Superclass

        Create a new object of the class itkBlockMatchingImageFilterID3_Superclass and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBlockMatchingImageFilterID3_Superclass.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkBlockMatchingImageFilterID3_Superclass.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkBlockMatchingImageFilterID3_Superclass.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBlockMatchingImageFilterID3_Superclass in _itkBlockMatchingImageFilterPython:
_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_swigregister(itkBlockMatchingImageFilterID3_Superclass)
itkBlockMatchingImageFilterID3_Superclass___New_orig__ = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass___New_orig__
itkBlockMatchingImageFilterID3_Superclass_cast = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Superclass_cast

class itkBlockMatchingImageFilterIF3_Superclass(itkBlockMatchingImageFilterIF3_Superclass_Superclass):
    r"""Proxy of C++ itkBlockMatchingImageFilterIF3_Superclass class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass___New_orig__)
    Clone = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_Clone)
    SetInput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_SetInput)
    GetInput = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_GetInput)
    __swig_destroy__ = _itkBlockMatchingImageFilterPython.delete_itkBlockMatchingImageFilterIF3_Superclass
    cast = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_cast)

    def New(*args, **kargs):
        """New() -> itkBlockMatchingImageFilterIF3_Superclass

        Create a new object of the class itkBlockMatchingImageFilterIF3_Superclass and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBlockMatchingImageFilterIF3_Superclass.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkBlockMatchingImageFilterIF3_Superclass.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkBlockMatchingImageFilterIF3_Superclass.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBlockMatchingImageFilterIF3_Superclass in _itkBlockMatchingImageFilterPython:
_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_swigregister(itkBlockMatchingImageFilterIF3_Superclass)
itkBlockMatchingImageFilterIF3_Superclass___New_orig__ = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass___New_orig__
itkBlockMatchingImageFilterIF3_Superclass_cast = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Superclass_cast

class itkBlockMatchingImageFilterID3(itkBlockMatchingImageFilterIF3_Superclass):
    r"""Proxy of C++ itkBlockMatchingImageFilterID3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3___New_orig__)
    Clone = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_Clone)
    SetBlockRadius = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_SetBlockRadius)
    GetBlockRadius = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_GetBlockRadius)
    SetSearchRadius = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_SetSearchRadius)
    GetSearchRadius = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_GetSearchRadius)
    SetFixedImage = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_SetFixedImage)
    GetFixedImage = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_GetFixedImage)
    SetMovingImage = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_SetMovingImage)
    GetMovingImage = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_GetMovingImage)
    SetFeaturePoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_SetFeaturePoints)
    GetFeaturePoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_GetFeaturePoints)
    GetDisplacements = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_GetDisplacements)
    GetSimilarities = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_GetSimilarities)
    __swig_destroy__ = _itkBlockMatchingImageFilterPython.delete_itkBlockMatchingImageFilterID3
    cast = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_cast)

    def New(*args, **kargs):
        """New() -> itkBlockMatchingImageFilterID3

        Create a new object of the class itkBlockMatchingImageFilterID3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBlockMatchingImageFilterID3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkBlockMatchingImageFilterID3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkBlockMatchingImageFilterID3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBlockMatchingImageFilterID3 in _itkBlockMatchingImageFilterPython:
_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_swigregister(itkBlockMatchingImageFilterID3)
itkBlockMatchingImageFilterID3___New_orig__ = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3___New_orig__
itkBlockMatchingImageFilterID3_cast = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterID3_cast

class itkBlockMatchingImageFilterIF3(itkBlockMatchingImageFilterIF3_Superclass):
    r"""Proxy of C++ itkBlockMatchingImageFilterIF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3___New_orig__)
    Clone = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_Clone)
    SetBlockRadius = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_SetBlockRadius)
    GetBlockRadius = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_GetBlockRadius)
    SetSearchRadius = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_SetSearchRadius)
    GetSearchRadius = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_GetSearchRadius)
    SetFixedImage = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_SetFixedImage)
    GetFixedImage = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_GetFixedImage)
    SetMovingImage = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_SetMovingImage)
    GetMovingImage = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_GetMovingImage)
    SetFeaturePoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_SetFeaturePoints)
    GetFeaturePoints = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_GetFeaturePoints)
    GetDisplacements = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_GetDisplacements)
    GetSimilarities = _swig_new_instance_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_GetSimilarities)
    __swig_destroy__ = _itkBlockMatchingImageFilterPython.delete_itkBlockMatchingImageFilterIF3
    cast = _swig_new_static_method(_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_cast)

    def New(*args, **kargs):
        """New() -> itkBlockMatchingImageFilterIF3

        Create a new object of the class itkBlockMatchingImageFilterIF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBlockMatchingImageFilterIF3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkBlockMatchingImageFilterIF3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkBlockMatchingImageFilterIF3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBlockMatchingImageFilterIF3 in _itkBlockMatchingImageFilterPython:
_itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_swigregister(itkBlockMatchingImageFilterIF3)
itkBlockMatchingImageFilterIF3___New_orig__ = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3___New_orig__
itkBlockMatchingImageFilterIF3_cast = _itkBlockMatchingImageFilterPython.itkBlockMatchingImageFilterIF3_cast


import itkHelpers
@itkHelpers.accept_numpy_array_like_xarray
def mesh_to_mesh_filter(*args, **kwargs):
    """Procedural interface for MeshToMeshFilter"""
    import itk
    instance = itk.MeshToMeshFilter.New(*args, **kwargs)
    return instance.__internal_call__()

def mesh_to_mesh_filter_init_docstring():
    import itk
    import itkTemplate
    if isinstance(itk.MeshToMeshFilter, itkTemplate.itkTemplate):
        mesh_to_mesh_filter.__doc__ = itk.MeshToMeshFilter.values()[0].__doc__
    else:
        mesh_to_mesh_filter.__doc__ = itk.MeshToMeshFilter.__doc__

import itkHelpers
@itkHelpers.accept_numpy_array_like_xarray
def block_matching_image_filter(*args, **kwargs):
    """Procedural interface for BlockMatchingImageFilter"""
    import itk
    instance = itk.BlockMatchingImageFilter.New(*args, **kwargs)
    return instance.__internal_call__()

def block_matching_image_filter_init_docstring():
    import itk
    import itkTemplate
    if isinstance(itk.BlockMatchingImageFilter, itkTemplate.itkTemplate):
        block_matching_image_filter.__doc__ = itk.BlockMatchingImageFilter.values()[0].__doc__
    else:
        block_matching_image_filter.__doc__ = itk.BlockMatchingImageFilter.__doc__

import itkHelpers
@itkHelpers.accept_numpy_array_like_xarray
def mesh_source(*args, **kwargs):
    """Procedural interface for MeshSource"""
    import itk
    instance = itk.MeshSource.New(*args, **kwargs)
    return instance.__internal_call__()

def mesh_source_init_docstring():
    import itk
    import itkTemplate
    if isinstance(itk.MeshSource, itkTemplate.itkTemplate):
        mesh_source.__doc__ = itk.MeshSource.values()[0].__doc__
    else:
        mesh_source.__doc__ = itk.MeshSource.__doc__




