# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _itkCorrelationImageToImageMetricv4Python.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_itkCorrelationImageToImageMetricv4Python', [dirname(__file__)])
        except ImportError:
            import _itkCorrelationImageToImageMetricv4Python
            return _itkCorrelationImageToImageMetricv4Python
        if fp is not None:
            try:
                _mod = imp.load_module('_itkCorrelationImageToImageMetricv4Python', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _itkCorrelationImageToImageMetricv4Python = swig_import_helper()
    del swig_import_helper
else:
    import _itkCorrelationImageToImageMetricv4Python
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


import itkImageToImageMetricv4Python
import itkPointSetPython
import ITKCommonBasePython
import pyBasePython
import itkMatrixPython
import vnl_vectorPython
import vnl_matrixPython
import stdcomplexPython
import vnl_matrix_fixedPython
import itkVectorPython
import vnl_vector_refPython
import itkFixedArrayPython
import itkPointPython
import itkCovariantVectorPython
import itkVectorContainerPython
import itkContinuousIndexPython
import itkIndexPython
import itkSizePython
import itkOffsetPython
import itkImageRegionPython
import itkOptimizerParametersPython
import itkArrayPython
import itkDisplacementFieldTransformPython
import itkDiffusionTensor3DPython
import itkSymmetricSecondRankTensorPython
import itkArray2DPython
import itkImagePython
import itkRGBAPixelPython
import itkRGBPixelPython
import itkVariableLengthVectorPython
import itkTransformBasePython
import itkObjectToObjectMetricBasePython
import itkSingleValuedCostFunctionv4Python
import itkCostFunctionPython
import itkImageToImageFilterBPython
import itkImageToImageFilterCommonPython
import itkVectorImagePython
import itkImageSourcePython
import itkImageSourceCommonPython
import itkInterpolateImageFunctionPython
import itkImageFunctionBasePython
import itkFunctionBasePython
import itkSpatialObjectBasePython
import itkSpatialObjectPropertyPython
import itkAffineTransformPython
import itkMatrixOffsetTransformBasePython
import itkBoundingBoxPython
import itkMapContainerPython

def itkCorrelationImageToImageMetricv4ID3ID3_New():
  return itkCorrelationImageToImageMetricv4ID3ID3.New()


def itkCorrelationImageToImageMetricv4ID2ID2_New():
  return itkCorrelationImageToImageMetricv4ID2ID2.New()


def itkCorrelationImageToImageMetricv4IF3IF3_New():
  return itkCorrelationImageToImageMetricv4IF3IF3.New()


def itkCorrelationImageToImageMetricv4IF2IF2_New():
  return itkCorrelationImageToImageMetricv4IF2IF2.New()

class itkCorrelationImageToImageMetricv4ID2ID2(itkImageToImageMetricv4Python.itkImageToImageMetricv4D2D2):
    """


    Class implementing normalized cross correlation image metric.

    Definition of the normalized cross correlation metric used here:

    negative square of normalized cross correlation

    \\[ C(f, m) = -\\frac{<f-\\bar{f}, m-\\bar{m}
    >^2}{|f-\\bar{f}|^2 |m-\\bar{m}|^2} \\]

    in which, f, m are the vectors of image pixel intensities,
    $\\bar{f}$ and $\\bar{m}$ are the mean values of f and m. <,>
    denotes inner product, $|\\cdot|$ denotes the 2-norm of the vector.
    The minus sign makes the metric to optimize towards its minimal value.
    Note that this uses the square of the mathematical notion of
    normalized cross correlation to avoid the square root computation in
    practice.

    Moving image (m) is a function of the parameters (p) of the moving
    transforms. So $ C(f, m) = C(f, m(p)) $ GetValueAndDerivative will
    return the value as $ C(f,m) $ and the derivative as

    \\[ \\frac{d}{dp} C = 2 \\frac{<f1, m1>}{|f1|^2 |m1|^2} * ( <f1,
    \\frac{dm}{dp}> - \\frac{<f1, m1>}{|m1|^2} < m1, \\frac{dm}{dp}
    > ) \\]

    in which, $ f1 = f - \\bar{f} $, $ m1 = m - \\bar{m} $ (Note:
    there should be a minus sign of $ \\frac{d}{dp} $ mathematically,
    which is not in the implementation to match the requirement of the
    metricv4 optimization framework.

    See CorrelationImageToImageMetricv4GetValueAndDerivativeThreader::Proc
    essPoint for algorithm implementation.

    This metric only works with the global transform. It throws an
    exception if the transform has local support.

    C++ includes: itkCorrelationImageToImageMetricv4.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkCorrelationImageToImageMetricv4ID2ID2_Pointer":
        """__New_orig__() -> itkCorrelationImageToImageMetricv4ID2ID2_Pointer"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID2ID2___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkCorrelationImageToImageMetricv4ID2ID2_Pointer":
        """Clone(itkCorrelationImageToImageMetricv4ID2ID2 self) -> itkCorrelationImageToImageMetricv4ID2ID2_Pointer"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID2ID2_Clone(self)

    __swig_destroy__ = _itkCorrelationImageToImageMetricv4Python.delete_itkCorrelationImageToImageMetricv4ID2ID2

    def cast(obj: 'itkLightObject') -> "itkCorrelationImageToImageMetricv4ID2ID2 *":
        """cast(itkLightObject obj) -> itkCorrelationImageToImageMetricv4ID2ID2"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID2ID2_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkCorrelationImageToImageMetricv4ID2ID2

        Create a new object of the class itkCorrelationImageToImageMetricv4ID2ID2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkCorrelationImageToImageMetricv4ID2ID2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkCorrelationImageToImageMetricv4ID2ID2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkCorrelationImageToImageMetricv4ID2ID2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkCorrelationImageToImageMetricv4ID2ID2.Clone = new_instancemethod(_itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID2ID2_Clone, None, itkCorrelationImageToImageMetricv4ID2ID2)
itkCorrelationImageToImageMetricv4ID2ID2_swigregister = _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID2ID2_swigregister
itkCorrelationImageToImageMetricv4ID2ID2_swigregister(itkCorrelationImageToImageMetricv4ID2ID2)

def itkCorrelationImageToImageMetricv4ID2ID2___New_orig__() -> "itkCorrelationImageToImageMetricv4ID2ID2_Pointer":
    """itkCorrelationImageToImageMetricv4ID2ID2___New_orig__() -> itkCorrelationImageToImageMetricv4ID2ID2_Pointer"""
    return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID2ID2___New_orig__()

def itkCorrelationImageToImageMetricv4ID2ID2_cast(obj: 'itkLightObject') -> "itkCorrelationImageToImageMetricv4ID2ID2 *":
    """itkCorrelationImageToImageMetricv4ID2ID2_cast(itkLightObject obj) -> itkCorrelationImageToImageMetricv4ID2ID2"""
    return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID2ID2_cast(obj)

class itkCorrelationImageToImageMetricv4ID3ID3(itkImageToImageMetricv4Python.itkImageToImageMetricv4D3D3):
    """


    Class implementing normalized cross correlation image metric.

    Definition of the normalized cross correlation metric used here:

    negative square of normalized cross correlation

    \\[ C(f, m) = -\\frac{<f-\\bar{f}, m-\\bar{m}
    >^2}{|f-\\bar{f}|^2 |m-\\bar{m}|^2} \\]

    in which, f, m are the vectors of image pixel intensities,
    $\\bar{f}$ and $\\bar{m}$ are the mean values of f and m. <,>
    denotes inner product, $|\\cdot|$ denotes the 2-norm of the vector.
    The minus sign makes the metric to optimize towards its minimal value.
    Note that this uses the square of the mathematical notion of
    normalized cross correlation to avoid the square root computation in
    practice.

    Moving image (m) is a function of the parameters (p) of the moving
    transforms. So $ C(f, m) = C(f, m(p)) $ GetValueAndDerivative will
    return the value as $ C(f,m) $ and the derivative as

    \\[ \\frac{d}{dp} C = 2 \\frac{<f1, m1>}{|f1|^2 |m1|^2} * ( <f1,
    \\frac{dm}{dp}> - \\frac{<f1, m1>}{|m1|^2} < m1, \\frac{dm}{dp}
    > ) \\]

    in which, $ f1 = f - \\bar{f} $, $ m1 = m - \\bar{m} $ (Note:
    there should be a minus sign of $ \\frac{d}{dp} $ mathematically,
    which is not in the implementation to match the requirement of the
    metricv4 optimization framework.

    See CorrelationImageToImageMetricv4GetValueAndDerivativeThreader::Proc
    essPoint for algorithm implementation.

    This metric only works with the global transform. It throws an
    exception if the transform has local support.

    C++ includes: itkCorrelationImageToImageMetricv4.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkCorrelationImageToImageMetricv4ID3ID3_Pointer":
        """__New_orig__() -> itkCorrelationImageToImageMetricv4ID3ID3_Pointer"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID3ID3___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkCorrelationImageToImageMetricv4ID3ID3_Pointer":
        """Clone(itkCorrelationImageToImageMetricv4ID3ID3 self) -> itkCorrelationImageToImageMetricv4ID3ID3_Pointer"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID3ID3_Clone(self)

    __swig_destroy__ = _itkCorrelationImageToImageMetricv4Python.delete_itkCorrelationImageToImageMetricv4ID3ID3

    def cast(obj: 'itkLightObject') -> "itkCorrelationImageToImageMetricv4ID3ID3 *":
        """cast(itkLightObject obj) -> itkCorrelationImageToImageMetricv4ID3ID3"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID3ID3_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkCorrelationImageToImageMetricv4ID3ID3

        Create a new object of the class itkCorrelationImageToImageMetricv4ID3ID3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkCorrelationImageToImageMetricv4ID3ID3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkCorrelationImageToImageMetricv4ID3ID3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkCorrelationImageToImageMetricv4ID3ID3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkCorrelationImageToImageMetricv4ID3ID3.Clone = new_instancemethod(_itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID3ID3_Clone, None, itkCorrelationImageToImageMetricv4ID3ID3)
itkCorrelationImageToImageMetricv4ID3ID3_swigregister = _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID3ID3_swigregister
itkCorrelationImageToImageMetricv4ID3ID3_swigregister(itkCorrelationImageToImageMetricv4ID3ID3)

def itkCorrelationImageToImageMetricv4ID3ID3___New_orig__() -> "itkCorrelationImageToImageMetricv4ID3ID3_Pointer":
    """itkCorrelationImageToImageMetricv4ID3ID3___New_orig__() -> itkCorrelationImageToImageMetricv4ID3ID3_Pointer"""
    return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID3ID3___New_orig__()

def itkCorrelationImageToImageMetricv4ID3ID3_cast(obj: 'itkLightObject') -> "itkCorrelationImageToImageMetricv4ID3ID3 *":
    """itkCorrelationImageToImageMetricv4ID3ID3_cast(itkLightObject obj) -> itkCorrelationImageToImageMetricv4ID3ID3"""
    return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4ID3ID3_cast(obj)

class itkCorrelationImageToImageMetricv4IF2IF2(itkImageToImageMetricv4Python.itkImageToImageMetricv4F2F2):
    """


    Class implementing normalized cross correlation image metric.

    Definition of the normalized cross correlation metric used here:

    negative square of normalized cross correlation

    \\[ C(f, m) = -\\frac{<f-\\bar{f}, m-\\bar{m}
    >^2}{|f-\\bar{f}|^2 |m-\\bar{m}|^2} \\]

    in which, f, m are the vectors of image pixel intensities,
    $\\bar{f}$ and $\\bar{m}$ are the mean values of f and m. <,>
    denotes inner product, $|\\cdot|$ denotes the 2-norm of the vector.
    The minus sign makes the metric to optimize towards its minimal value.
    Note that this uses the square of the mathematical notion of
    normalized cross correlation to avoid the square root computation in
    practice.

    Moving image (m) is a function of the parameters (p) of the moving
    transforms. So $ C(f, m) = C(f, m(p)) $ GetValueAndDerivative will
    return the value as $ C(f,m) $ and the derivative as

    \\[ \\frac{d}{dp} C = 2 \\frac{<f1, m1>}{|f1|^2 |m1|^2} * ( <f1,
    \\frac{dm}{dp}> - \\frac{<f1, m1>}{|m1|^2} < m1, \\frac{dm}{dp}
    > ) \\]

    in which, $ f1 = f - \\bar{f} $, $ m1 = m - \\bar{m} $ (Note:
    there should be a minus sign of $ \\frac{d}{dp} $ mathematically,
    which is not in the implementation to match the requirement of the
    metricv4 optimization framework.

    See CorrelationImageToImageMetricv4GetValueAndDerivativeThreader::Proc
    essPoint for algorithm implementation.

    This metric only works with the global transform. It throws an
    exception if the transform has local support.

    C++ includes: itkCorrelationImageToImageMetricv4.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkCorrelationImageToImageMetricv4IF2IF2_Pointer":
        """__New_orig__() -> itkCorrelationImageToImageMetricv4IF2IF2_Pointer"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF2IF2___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkCorrelationImageToImageMetricv4IF2IF2_Pointer":
        """Clone(itkCorrelationImageToImageMetricv4IF2IF2 self) -> itkCorrelationImageToImageMetricv4IF2IF2_Pointer"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF2IF2_Clone(self)

    __swig_destroy__ = _itkCorrelationImageToImageMetricv4Python.delete_itkCorrelationImageToImageMetricv4IF2IF2

    def cast(obj: 'itkLightObject') -> "itkCorrelationImageToImageMetricv4IF2IF2 *":
        """cast(itkLightObject obj) -> itkCorrelationImageToImageMetricv4IF2IF2"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF2IF2_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkCorrelationImageToImageMetricv4IF2IF2

        Create a new object of the class itkCorrelationImageToImageMetricv4IF2IF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkCorrelationImageToImageMetricv4IF2IF2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkCorrelationImageToImageMetricv4IF2IF2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkCorrelationImageToImageMetricv4IF2IF2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkCorrelationImageToImageMetricv4IF2IF2.Clone = new_instancemethod(_itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF2IF2_Clone, None, itkCorrelationImageToImageMetricv4IF2IF2)
itkCorrelationImageToImageMetricv4IF2IF2_swigregister = _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF2IF2_swigregister
itkCorrelationImageToImageMetricv4IF2IF2_swigregister(itkCorrelationImageToImageMetricv4IF2IF2)

def itkCorrelationImageToImageMetricv4IF2IF2___New_orig__() -> "itkCorrelationImageToImageMetricv4IF2IF2_Pointer":
    """itkCorrelationImageToImageMetricv4IF2IF2___New_orig__() -> itkCorrelationImageToImageMetricv4IF2IF2_Pointer"""
    return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF2IF2___New_orig__()

def itkCorrelationImageToImageMetricv4IF2IF2_cast(obj: 'itkLightObject') -> "itkCorrelationImageToImageMetricv4IF2IF2 *":
    """itkCorrelationImageToImageMetricv4IF2IF2_cast(itkLightObject obj) -> itkCorrelationImageToImageMetricv4IF2IF2"""
    return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF2IF2_cast(obj)

class itkCorrelationImageToImageMetricv4IF3IF3(itkImageToImageMetricv4Python.itkImageToImageMetricv4F3F3):
    """


    Class implementing normalized cross correlation image metric.

    Definition of the normalized cross correlation metric used here:

    negative square of normalized cross correlation

    \\[ C(f, m) = -\\frac{<f-\\bar{f}, m-\\bar{m}
    >^2}{|f-\\bar{f}|^2 |m-\\bar{m}|^2} \\]

    in which, f, m are the vectors of image pixel intensities,
    $\\bar{f}$ and $\\bar{m}$ are the mean values of f and m. <,>
    denotes inner product, $|\\cdot|$ denotes the 2-norm of the vector.
    The minus sign makes the metric to optimize towards its minimal value.
    Note that this uses the square of the mathematical notion of
    normalized cross correlation to avoid the square root computation in
    practice.

    Moving image (m) is a function of the parameters (p) of the moving
    transforms. So $ C(f, m) = C(f, m(p)) $ GetValueAndDerivative will
    return the value as $ C(f,m) $ and the derivative as

    \\[ \\frac{d}{dp} C = 2 \\frac{<f1, m1>}{|f1|^2 |m1|^2} * ( <f1,
    \\frac{dm}{dp}> - \\frac{<f1, m1>}{|m1|^2} < m1, \\frac{dm}{dp}
    > ) \\]

    in which, $ f1 = f - \\bar{f} $, $ m1 = m - \\bar{m} $ (Note:
    there should be a minus sign of $ \\frac{d}{dp} $ mathematically,
    which is not in the implementation to match the requirement of the
    metricv4 optimization framework.

    See CorrelationImageToImageMetricv4GetValueAndDerivativeThreader::Proc
    essPoint for algorithm implementation.

    This metric only works with the global transform. It throws an
    exception if the transform has local support.

    C++ includes: itkCorrelationImageToImageMetricv4.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkCorrelationImageToImageMetricv4IF3IF3_Pointer":
        """__New_orig__() -> itkCorrelationImageToImageMetricv4IF3IF3_Pointer"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF3IF3___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkCorrelationImageToImageMetricv4IF3IF3_Pointer":
        """Clone(itkCorrelationImageToImageMetricv4IF3IF3 self) -> itkCorrelationImageToImageMetricv4IF3IF3_Pointer"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF3IF3_Clone(self)

    __swig_destroy__ = _itkCorrelationImageToImageMetricv4Python.delete_itkCorrelationImageToImageMetricv4IF3IF3

    def cast(obj: 'itkLightObject') -> "itkCorrelationImageToImageMetricv4IF3IF3 *":
        """cast(itkLightObject obj) -> itkCorrelationImageToImageMetricv4IF3IF3"""
        return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF3IF3_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkCorrelationImageToImageMetricv4IF3IF3

        Create a new object of the class itkCorrelationImageToImageMetricv4IF3IF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkCorrelationImageToImageMetricv4IF3IF3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkCorrelationImageToImageMetricv4IF3IF3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkCorrelationImageToImageMetricv4IF3IF3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkCorrelationImageToImageMetricv4IF3IF3.Clone = new_instancemethod(_itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF3IF3_Clone, None, itkCorrelationImageToImageMetricv4IF3IF3)
itkCorrelationImageToImageMetricv4IF3IF3_swigregister = _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF3IF3_swigregister
itkCorrelationImageToImageMetricv4IF3IF3_swigregister(itkCorrelationImageToImageMetricv4IF3IF3)

def itkCorrelationImageToImageMetricv4IF3IF3___New_orig__() -> "itkCorrelationImageToImageMetricv4IF3IF3_Pointer":
    """itkCorrelationImageToImageMetricv4IF3IF3___New_orig__() -> itkCorrelationImageToImageMetricv4IF3IF3_Pointer"""
    return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF3IF3___New_orig__()

def itkCorrelationImageToImageMetricv4IF3IF3_cast(obj: 'itkLightObject') -> "itkCorrelationImageToImageMetricv4IF3IF3 *":
    """itkCorrelationImageToImageMetricv4IF3IF3_cast(itkLightObject obj) -> itkCorrelationImageToImageMetricv4IF3IF3"""
    return _itkCorrelationImageToImageMetricv4Python.itkCorrelationImageToImageMetricv4IF3IF3_cast(obj)



