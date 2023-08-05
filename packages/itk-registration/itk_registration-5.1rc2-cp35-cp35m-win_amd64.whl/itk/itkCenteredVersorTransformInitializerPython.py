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
    from . import _itkCenteredVersorTransformInitializerPython
else:
    import _itkCenteredVersorTransformInitializerPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkCenteredVersorTransformInitializerPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkCenteredVersorTransformInitializerPython.SWIG_PyStaticMethod_New

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
import itkCenteredTransformInitializerPython
import itkImageMomentsCalculatorPython
import itkMatrixPython
import vnl_matrixPython
import vnl_vectorPython
import stdcomplexPython
import vnl_matrix_fixedPython
import itkVectorPython
import vnl_vector_refPython
import itkFixedArrayPython
import itkCovariantVectorPython
import itkPointPython
import itkSpatialObjectBasePython
import itkImageRegionPython
import itkSizePython
import itkIndexPython
import itkOffsetPython
import itkSpatialObjectPropertyPython
import itkRGBAPixelPython
import itkAffineTransformPython
import itkTransformBasePython
import itkSymmetricSecondRankTensorPython
import itkOptimizerParametersPython
import itkArrayPython
import itkArray2DPython
import itkVariableLengthVectorPython
import itkDiffusionTensor3DPython
import itkMatrixOffsetTransformBasePython
import itkBoundingBoxPython
import itkMapContainerPython
import itkVectorContainerPython
import itkContinuousIndexPython
import itkImagePython
import itkRGBPixelPython
import itkCenteredRigid2DTransformPython
import itkRigid2DTransformPython
import itkVersorRigid3DTransformPython
import itkVersorTransformPython
import itkRigid3DTransformPython
import itkVersorPython

def itkCenteredVersorTransformInitializerID3ID3_New():
  return itkCenteredVersorTransformInitializerID3ID3.New()


def itkCenteredVersorTransformInitializerIF3IF3_New():
  return itkCenteredVersorTransformInitializerIF3IF3.New()


def itkCenteredVersorTransformInitializerIUS3IUS3_New():
  return itkCenteredVersorTransformInitializerIUS3IUS3.New()


def itkCenteredVersorTransformInitializerIUC3IUC3_New():
  return itkCenteredVersorTransformInitializerIUC3IUC3.New()


def itkCenteredVersorTransformInitializerISS3ISS3_New():
  return itkCenteredVersorTransformInitializerISS3ISS3.New()

class itkCenteredVersorTransformInitializerID3ID3(itkCenteredTransformInitializerPython.itkCenteredTransformInitializerVR3DTDID3ID3):
    r"""Proxy of C++ itkCenteredVersorTransformInitializerID3ID3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3___New_orig__)
    Clone = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3_Clone)
    SetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3_SetComputeRotation)
    GetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3_GetComputeRotation)
    ComputeRotationOn = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3_ComputeRotationOn)
    ComputeRotationOff = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3_ComputeRotationOff)
    __swig_destroy__ = _itkCenteredVersorTransformInitializerPython.delete_itkCenteredVersorTransformInitializerID3ID3
    cast = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3_cast)

    def New(*args, **kargs):
        """New() -> itkCenteredVersorTransformInitializerID3ID3

        Create a new object of the class itkCenteredVersorTransformInitializerID3ID3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkCenteredVersorTransformInitializerID3ID3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkCenteredVersorTransformInitializerID3ID3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkCenteredVersorTransformInitializerID3ID3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkCenteredVersorTransformInitializerID3ID3 in _itkCenteredVersorTransformInitializerPython:
_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3_swigregister(itkCenteredVersorTransformInitializerID3ID3)
itkCenteredVersorTransformInitializerID3ID3___New_orig__ = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3___New_orig__
itkCenteredVersorTransformInitializerID3ID3_cast = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerID3ID3_cast

class itkCenteredVersorTransformInitializerIF3IF3(itkCenteredTransformInitializerPython.itkCenteredTransformInitializerVR3DTDIF3IF3):
    r"""Proxy of C++ itkCenteredVersorTransformInitializerIF3IF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3___New_orig__)
    Clone = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3_Clone)
    SetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3_SetComputeRotation)
    GetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3_GetComputeRotation)
    ComputeRotationOn = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3_ComputeRotationOn)
    ComputeRotationOff = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3_ComputeRotationOff)
    __swig_destroy__ = _itkCenteredVersorTransformInitializerPython.delete_itkCenteredVersorTransformInitializerIF3IF3
    cast = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3_cast)

    def New(*args, **kargs):
        """New() -> itkCenteredVersorTransformInitializerIF3IF3

        Create a new object of the class itkCenteredVersorTransformInitializerIF3IF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkCenteredVersorTransformInitializerIF3IF3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkCenteredVersorTransformInitializerIF3IF3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkCenteredVersorTransformInitializerIF3IF3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkCenteredVersorTransformInitializerIF3IF3 in _itkCenteredVersorTransformInitializerPython:
_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3_swigregister(itkCenteredVersorTransformInitializerIF3IF3)
itkCenteredVersorTransformInitializerIF3IF3___New_orig__ = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3___New_orig__
itkCenteredVersorTransformInitializerIF3IF3_cast = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIF3IF3_cast

class itkCenteredVersorTransformInitializerISS3ISS3(itkCenteredTransformInitializerPython.itkCenteredTransformInitializerVR3DTDISS3ISS3):
    r"""Proxy of C++ itkCenteredVersorTransformInitializerISS3ISS3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3___New_orig__)
    Clone = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3_Clone)
    SetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3_SetComputeRotation)
    GetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3_GetComputeRotation)
    ComputeRotationOn = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3_ComputeRotationOn)
    ComputeRotationOff = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3_ComputeRotationOff)
    __swig_destroy__ = _itkCenteredVersorTransformInitializerPython.delete_itkCenteredVersorTransformInitializerISS3ISS3
    cast = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3_cast)

    def New(*args, **kargs):
        """New() -> itkCenteredVersorTransformInitializerISS3ISS3

        Create a new object of the class itkCenteredVersorTransformInitializerISS3ISS3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkCenteredVersorTransformInitializerISS3ISS3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkCenteredVersorTransformInitializerISS3ISS3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkCenteredVersorTransformInitializerISS3ISS3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkCenteredVersorTransformInitializerISS3ISS3 in _itkCenteredVersorTransformInitializerPython:
_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3_swigregister(itkCenteredVersorTransformInitializerISS3ISS3)
itkCenteredVersorTransformInitializerISS3ISS3___New_orig__ = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3___New_orig__
itkCenteredVersorTransformInitializerISS3ISS3_cast = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerISS3ISS3_cast

class itkCenteredVersorTransformInitializerIUC3IUC3(itkCenteredTransformInitializerPython.itkCenteredTransformInitializerVR3DTDIUC3IUC3):
    r"""Proxy of C++ itkCenteredVersorTransformInitializerIUC3IUC3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3___New_orig__)
    Clone = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3_Clone)
    SetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3_SetComputeRotation)
    GetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3_GetComputeRotation)
    ComputeRotationOn = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3_ComputeRotationOn)
    ComputeRotationOff = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3_ComputeRotationOff)
    __swig_destroy__ = _itkCenteredVersorTransformInitializerPython.delete_itkCenteredVersorTransformInitializerIUC3IUC3
    cast = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3_cast)

    def New(*args, **kargs):
        """New() -> itkCenteredVersorTransformInitializerIUC3IUC3

        Create a new object of the class itkCenteredVersorTransformInitializerIUC3IUC3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkCenteredVersorTransformInitializerIUC3IUC3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkCenteredVersorTransformInitializerIUC3IUC3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkCenteredVersorTransformInitializerIUC3IUC3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkCenteredVersorTransformInitializerIUC3IUC3 in _itkCenteredVersorTransformInitializerPython:
_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3_swigregister(itkCenteredVersorTransformInitializerIUC3IUC3)
itkCenteredVersorTransformInitializerIUC3IUC3___New_orig__ = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3___New_orig__
itkCenteredVersorTransformInitializerIUC3IUC3_cast = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUC3IUC3_cast

class itkCenteredVersorTransformInitializerIUS3IUS3(itkCenteredTransformInitializerPython.itkCenteredTransformInitializerVR3DTDIUS3IUS3):
    r"""Proxy of C++ itkCenteredVersorTransformInitializerIUS3IUS3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3___New_orig__)
    Clone = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3_Clone)
    SetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3_SetComputeRotation)
    GetComputeRotation = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3_GetComputeRotation)
    ComputeRotationOn = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3_ComputeRotationOn)
    ComputeRotationOff = _swig_new_instance_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3_ComputeRotationOff)
    __swig_destroy__ = _itkCenteredVersorTransformInitializerPython.delete_itkCenteredVersorTransformInitializerIUS3IUS3
    cast = _swig_new_static_method(_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3_cast)

    def New(*args, **kargs):
        """New() -> itkCenteredVersorTransformInitializerIUS3IUS3

        Create a new object of the class itkCenteredVersorTransformInitializerIUS3IUS3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkCenteredVersorTransformInitializerIUS3IUS3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkCenteredVersorTransformInitializerIUS3IUS3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkCenteredVersorTransformInitializerIUS3IUS3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkCenteredVersorTransformInitializerIUS3IUS3 in _itkCenteredVersorTransformInitializerPython:
_itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3_swigregister(itkCenteredVersorTransformInitializerIUS3IUS3)
itkCenteredVersorTransformInitializerIUS3IUS3___New_orig__ = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3___New_orig__
itkCenteredVersorTransformInitializerIUS3IUS3_cast = _itkCenteredVersorTransformInitializerPython.itkCenteredVersorTransformInitializerIUS3IUS3_cast



