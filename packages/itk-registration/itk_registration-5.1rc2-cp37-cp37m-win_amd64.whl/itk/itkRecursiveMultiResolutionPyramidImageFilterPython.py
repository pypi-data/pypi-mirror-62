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
    from . import _itkRecursiveMultiResolutionPyramidImageFilterPython
else:
    import _itkRecursiveMultiResolutionPyramidImageFilterPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkRecursiveMultiResolutionPyramidImageFilterPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkRecursiveMultiResolutionPyramidImageFilterPython.SWIG_PyStaticMethod_New

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


import itkMultiResolutionPyramidImageFilterPython
import itkImageToImageFilterAPython
import itkImageToImageFilterCommonPython
import pyBasePython
import itkImageRegionPython
import ITKCommonBasePython
import itkSizePython
import itkIndexPython
import itkOffsetPython
import itkVectorImagePython
import stdcomplexPython
import itkVariableLengthVectorPython
import itkImagePython
import itkRGBAPixelPython
import itkFixedArrayPython
import itkMatrixPython
import vnl_matrix_fixedPython
import vnl_matrixPython
import vnl_vectorPython
import itkVectorPython
import vnl_vector_refPython
import itkPointPython
import itkCovariantVectorPython
import itkRGBPixelPython
import itkSymmetricSecondRankTensorPython
import itkImageSourcePython
import itkImageSourceCommonPython
import itkArray2DPython

def itkRecursiveMultiResolutionPyramidImageFilterID3ID3_New():
  return itkRecursiveMultiResolutionPyramidImageFilterID3ID3.New()


def itkRecursiveMultiResolutionPyramidImageFilterID2ID2_New():
  return itkRecursiveMultiResolutionPyramidImageFilterID2ID2.New()


def itkRecursiveMultiResolutionPyramidImageFilterIF3IF3_New():
  return itkRecursiveMultiResolutionPyramidImageFilterIF3IF3.New()


def itkRecursiveMultiResolutionPyramidImageFilterIF2IF2_New():
  return itkRecursiveMultiResolutionPyramidImageFilterIF2IF2.New()


def itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3_New():
  return itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3.New()


def itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2_New():
  return itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2.New()


def itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3_New():
  return itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3.New()


def itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2_New():
  return itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2.New()


def itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3_New():
  return itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3.New()


def itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2_New():
  return itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2.New()

class itkRecursiveMultiResolutionPyramidImageFilterID2ID2(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterID2ID2):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterID2ID2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID2ID2___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID2ID2_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterID2ID2
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID2ID2_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterID2ID2

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterID2ID2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterID2ID2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterID2ID2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterID2ID2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterID2ID2 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID2ID2_swigregister(itkRecursiveMultiResolutionPyramidImageFilterID2ID2)
itkRecursiveMultiResolutionPyramidImageFilterID2ID2___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID2ID2___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterID2ID2_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID2ID2_cast

class itkRecursiveMultiResolutionPyramidImageFilterID3ID3(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterID3ID3):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterID3ID3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID3ID3___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID3ID3_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterID3ID3
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID3ID3_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterID3ID3

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterID3ID3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterID3ID3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterID3ID3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterID3ID3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterID3ID3 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID3ID3_swigregister(itkRecursiveMultiResolutionPyramidImageFilterID3ID3)
itkRecursiveMultiResolutionPyramidImageFilterID3ID3___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID3ID3___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterID3ID3_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterID3ID3_cast

class itkRecursiveMultiResolutionPyramidImageFilterIF2IF2(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterIF2IF2):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterIF2IF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF2IF2___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF2IF2_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterIF2IF2
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF2IF2_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterIF2IF2

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterIF2IF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterIF2IF2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterIF2IF2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterIF2IF2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterIF2IF2 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF2IF2_swigregister(itkRecursiveMultiResolutionPyramidImageFilterIF2IF2)
itkRecursiveMultiResolutionPyramidImageFilterIF2IF2___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF2IF2___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterIF2IF2_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF2IF2_cast

class itkRecursiveMultiResolutionPyramidImageFilterIF3IF3(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterIF3IF3):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterIF3IF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF3IF3___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF3IF3_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterIF3IF3
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF3IF3_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterIF3IF3

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterIF3IF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterIF3IF3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterIF3IF3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterIF3IF3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterIF3IF3 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF3IF3_swigregister(itkRecursiveMultiResolutionPyramidImageFilterIF3IF3)
itkRecursiveMultiResolutionPyramidImageFilterIF3IF3___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF3IF3___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterIF3IF3_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIF3IF3_cast

class itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterISS2ISS2):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2_swigregister(itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2)
itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS2ISS2_cast

class itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterISS3ISS3):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3_swigregister(itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3)
itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterISS3ISS3_cast

class itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterIUC2IUC2):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2_swigregister(itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2)
itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC2IUC2_cast

class itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterIUC3IUC3):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3_swigregister(itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3)
itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUC3IUC3_cast

class itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterIUS2IUS2):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2_swigregister(itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2)
itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS2IUS2_cast

class itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3(itkMultiResolutionPyramidImageFilterPython.itkMultiResolutionPyramidImageFilterIUS3IUS3):
    r"""Proxy of C++ itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3___New_orig__)
    Clone = _swig_new_instance_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3_Clone)
    __swig_destroy__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.delete_itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3
    cast = _swig_new_static_method(_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3_cast)

    def New(*args, **kargs):
        """New() -> itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3

        Create a new object of the class itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3 in _itkRecursiveMultiResolutionPyramidImageFilterPython:
_itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3_swigregister(itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3)
itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3___New_orig__ = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3___New_orig__
itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3_cast = _itkRecursiveMultiResolutionPyramidImageFilterPython.itkRecursiveMultiResolutionPyramidImageFilterIUS3IUS3_cast


import itkHelpers
@itkHelpers.accept_numpy_array_like_xarray
def recursive_multi_resolution_pyramid_image_filter(*args, **kwargs):
    """Procedural interface for RecursiveMultiResolutionPyramidImageFilter"""
    import itk
    instance = itk.RecursiveMultiResolutionPyramidImageFilter.New(*args, **kwargs)
    return instance.__internal_call__()

def recursive_multi_resolution_pyramid_image_filter_init_docstring():
    import itk
    import itkTemplate
    if isinstance(itk.RecursiveMultiResolutionPyramidImageFilter, itkTemplate.itkTemplate):
        recursive_multi_resolution_pyramid_image_filter.__doc__ = itk.RecursiveMultiResolutionPyramidImageFilter.values()[0].__doc__
    else:
        recursive_multi_resolution_pyramid_image_filter.__doc__ = itk.RecursiveMultiResolutionPyramidImageFilter.__doc__




