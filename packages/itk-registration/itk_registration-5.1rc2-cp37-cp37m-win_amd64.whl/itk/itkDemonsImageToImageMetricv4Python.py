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
    from . import _itkDemonsImageToImageMetricv4Python
else:
    import _itkDemonsImageToImageMetricv4Python

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkDemonsImageToImageMetricv4Python.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkDemonsImageToImageMetricv4Python.SWIG_PyStaticMethod_New

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
import itkImageToImageMetricv4Python
import itkMatrixPython
import vnl_matrix_fixedPython
import vnl_matrixPython
import vnl_vectorPython
import stdcomplexPython
import itkVectorPython
import vnl_vector_refPython
import itkFixedArrayPython
import itkPointPython
import itkCovariantVectorPython
import itkObjectToObjectMetricBasePython
import itkArrayPython
import itkOptimizerParametersPython
import itkSingleValuedCostFunctionv4Python
import itkCostFunctionPython
import itkImagePython
import itkSizePython
import itkRGBAPixelPython
import itkImageRegionPython
import itkIndexPython
import itkOffsetPython
import itkRGBPixelPython
import itkSymmetricSecondRankTensorPython
import itkInterpolateImageFunctionPython
import itkContinuousIndexPython
import itkImageFunctionBasePython
import itkFunctionBasePython
import itkPointSetPython
import itkVectorContainerPython
import itkDisplacementFieldTransformPython
import itkArray2DPython
import itkVariableLengthVectorPython
import itkTransformBasePython
import itkDiffusionTensor3DPython
import itkSpatialObjectBasePython
import itkSpatialObjectPropertyPython
import itkAffineTransformPython
import itkMatrixOffsetTransformBasePython
import itkBoundingBoxPython
import itkMapContainerPython
import itkImageToImageFilterBPython
import itkImageToImageFilterCommonPython
import itkVectorImagePython
import itkImageSourcePython
import itkImageSourceCommonPython

def itkDemonsImageToImageMetricv4ID3ID3_New():
  return itkDemonsImageToImageMetricv4ID3ID3.New()


def itkDemonsImageToImageMetricv4ID2ID2_New():
  return itkDemonsImageToImageMetricv4ID2ID2.New()


def itkDemonsImageToImageMetricv4IF3IF3_New():
  return itkDemonsImageToImageMetricv4IF3IF3.New()


def itkDemonsImageToImageMetricv4IF2IF2_New():
  return itkDemonsImageToImageMetricv4IF2IF2.New()

class itkDemonsImageToImageMetricv4ID2ID2(itkImageToImageMetricv4Python.itkImageToImageMetricv4D2D2):
    r"""Proxy of C++ itkDemonsImageToImageMetricv4ID2ID2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID2ID2___New_orig__)
    Clone = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID2ID2_Clone)
    GetIntensityDifferenceThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID2ID2_GetIntensityDifferenceThreshold)
    SetIntensityDifferenceThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID2ID2_SetIntensityDifferenceThreshold)
    GetDenominatorThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID2ID2_GetDenominatorThreshold)
    __swig_destroy__ = _itkDemonsImageToImageMetricv4Python.delete_itkDemonsImageToImageMetricv4ID2ID2
    cast = _swig_new_static_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID2ID2_cast)

    def New(*args, **kargs):
        """New() -> itkDemonsImageToImageMetricv4ID2ID2

        Create a new object of the class itkDemonsImageToImageMetricv4ID2ID2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkDemonsImageToImageMetricv4ID2ID2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkDemonsImageToImageMetricv4ID2ID2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkDemonsImageToImageMetricv4ID2ID2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkDemonsImageToImageMetricv4ID2ID2 in _itkDemonsImageToImageMetricv4Python:
_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID2ID2_swigregister(itkDemonsImageToImageMetricv4ID2ID2)
itkDemonsImageToImageMetricv4ID2ID2___New_orig__ = _itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID2ID2___New_orig__
itkDemonsImageToImageMetricv4ID2ID2_cast = _itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID2ID2_cast

class itkDemonsImageToImageMetricv4ID3ID3(itkImageToImageMetricv4Python.itkImageToImageMetricv4D3D3):
    r"""Proxy of C++ itkDemonsImageToImageMetricv4ID3ID3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID3ID3___New_orig__)
    Clone = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID3ID3_Clone)
    GetIntensityDifferenceThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID3ID3_GetIntensityDifferenceThreshold)
    SetIntensityDifferenceThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID3ID3_SetIntensityDifferenceThreshold)
    GetDenominatorThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID3ID3_GetDenominatorThreshold)
    __swig_destroy__ = _itkDemonsImageToImageMetricv4Python.delete_itkDemonsImageToImageMetricv4ID3ID3
    cast = _swig_new_static_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID3ID3_cast)

    def New(*args, **kargs):
        """New() -> itkDemonsImageToImageMetricv4ID3ID3

        Create a new object of the class itkDemonsImageToImageMetricv4ID3ID3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkDemonsImageToImageMetricv4ID3ID3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkDemonsImageToImageMetricv4ID3ID3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkDemonsImageToImageMetricv4ID3ID3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkDemonsImageToImageMetricv4ID3ID3 in _itkDemonsImageToImageMetricv4Python:
_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID3ID3_swigregister(itkDemonsImageToImageMetricv4ID3ID3)
itkDemonsImageToImageMetricv4ID3ID3___New_orig__ = _itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID3ID3___New_orig__
itkDemonsImageToImageMetricv4ID3ID3_cast = _itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4ID3ID3_cast

class itkDemonsImageToImageMetricv4IF2IF2(itkImageToImageMetricv4Python.itkImageToImageMetricv4F2F2):
    r"""Proxy of C++ itkDemonsImageToImageMetricv4IF2IF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF2IF2___New_orig__)
    Clone = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF2IF2_Clone)
    GetIntensityDifferenceThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF2IF2_GetIntensityDifferenceThreshold)
    SetIntensityDifferenceThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF2IF2_SetIntensityDifferenceThreshold)
    GetDenominatorThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF2IF2_GetDenominatorThreshold)
    __swig_destroy__ = _itkDemonsImageToImageMetricv4Python.delete_itkDemonsImageToImageMetricv4IF2IF2
    cast = _swig_new_static_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF2IF2_cast)

    def New(*args, **kargs):
        """New() -> itkDemonsImageToImageMetricv4IF2IF2

        Create a new object of the class itkDemonsImageToImageMetricv4IF2IF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkDemonsImageToImageMetricv4IF2IF2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkDemonsImageToImageMetricv4IF2IF2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkDemonsImageToImageMetricv4IF2IF2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkDemonsImageToImageMetricv4IF2IF2 in _itkDemonsImageToImageMetricv4Python:
_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF2IF2_swigregister(itkDemonsImageToImageMetricv4IF2IF2)
itkDemonsImageToImageMetricv4IF2IF2___New_orig__ = _itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF2IF2___New_orig__
itkDemonsImageToImageMetricv4IF2IF2_cast = _itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF2IF2_cast

class itkDemonsImageToImageMetricv4IF3IF3(itkImageToImageMetricv4Python.itkImageToImageMetricv4F3F3):
    r"""Proxy of C++ itkDemonsImageToImageMetricv4IF3IF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF3IF3___New_orig__)
    Clone = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF3IF3_Clone)
    GetIntensityDifferenceThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF3IF3_GetIntensityDifferenceThreshold)
    SetIntensityDifferenceThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF3IF3_SetIntensityDifferenceThreshold)
    GetDenominatorThreshold = _swig_new_instance_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF3IF3_GetDenominatorThreshold)
    __swig_destroy__ = _itkDemonsImageToImageMetricv4Python.delete_itkDemonsImageToImageMetricv4IF3IF3
    cast = _swig_new_static_method(_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF3IF3_cast)

    def New(*args, **kargs):
        """New() -> itkDemonsImageToImageMetricv4IF3IF3

        Create a new object of the class itkDemonsImageToImageMetricv4IF3IF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkDemonsImageToImageMetricv4IF3IF3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkDemonsImageToImageMetricv4IF3IF3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkDemonsImageToImageMetricv4IF3IF3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkDemonsImageToImageMetricv4IF3IF3 in _itkDemonsImageToImageMetricv4Python:
_itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF3IF3_swigregister(itkDemonsImageToImageMetricv4IF3IF3)
itkDemonsImageToImageMetricv4IF3IF3___New_orig__ = _itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF3IF3___New_orig__
itkDemonsImageToImageMetricv4IF3IF3_cast = _itkDemonsImageToImageMetricv4Python.itkDemonsImageToImageMetricv4IF3IF3_cast



