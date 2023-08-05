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
    from . import _itkRegularStepGradientDescentOptimizerv4Python
else:
    import _itkRegularStepGradientDescentOptimizerv4Python

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkRegularStepGradientDescentOptimizerv4Python.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkRegularStepGradientDescentOptimizerv4Python.SWIG_PyStaticMethod_New

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
import itkGradientDescentOptimizerv4Python
import itkGradientDescentOptimizerBasev4Python
import itkArrayPython
import vnl_vectorPython
import vnl_matrixPython
import stdcomplexPython
import itkObjectToObjectOptimizerBasePython
import itkObjectToObjectMetricBasePython
import itkOptimizerParametersPython
import itkSingleValuedCostFunctionv4Python
import itkCostFunctionPython
import itkOptimizerParameterScalesEstimatorPython
import itkIndexPython
import itkSizePython
import itkOffsetPython

def itkRegularStepGradientDescentOptimizerv4F_New():
  return itkRegularStepGradientDescentOptimizerv4F.New()


def itkRegularStepGradientDescentOptimizerv4D_New():
  return itkRegularStepGradientDescentOptimizerv4D.New()

class itkRegularStepGradientDescentOptimizerv4D(itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD):
    r"""Proxy of C++ itkRegularStepGradientDescentOptimizerv4D class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D___New_orig__)
    Clone = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_Clone)
    SetMinimumStepLength = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_SetMinimumStepLength)
    GetMinimumStepLength = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_GetMinimumStepLength)
    SetRelaxationFactor = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_SetRelaxationFactor)
    GetRelaxationFactor = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_GetRelaxationFactor)
    SetGradientMagnitudeTolerance = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_SetGradientMagnitudeTolerance)
    GetGradientMagnitudeTolerance = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_GetGradientMagnitudeTolerance)
    SetCurrentLearningRateRelaxation = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_SetCurrentLearningRateRelaxation)
    GetCurrentLearningRateRelaxation = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_GetCurrentLearningRateRelaxation)
    StartOptimization = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_StartOptimization)
    GetCurrentStepLength = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_GetCurrentStepLength)
    __swig_destroy__ = _itkRegularStepGradientDescentOptimizerv4Python.delete_itkRegularStepGradientDescentOptimizerv4D
    cast = _swig_new_static_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_cast)

    def New(*args, **kargs):
        """New() -> itkRegularStepGradientDescentOptimizerv4D

        Create a new object of the class itkRegularStepGradientDescentOptimizerv4D and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRegularStepGradientDescentOptimizerv4D.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRegularStepGradientDescentOptimizerv4D.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRegularStepGradientDescentOptimizerv4D.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRegularStepGradientDescentOptimizerv4D in _itkRegularStepGradientDescentOptimizerv4Python:
_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_swigregister(itkRegularStepGradientDescentOptimizerv4D)
itkRegularStepGradientDescentOptimizerv4D___New_orig__ = _itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D___New_orig__
itkRegularStepGradientDescentOptimizerv4D_cast = _itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4D_cast

class itkRegularStepGradientDescentOptimizerv4F(itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF):
    r"""Proxy of C++ itkRegularStepGradientDescentOptimizerv4F class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F___New_orig__)
    Clone = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_Clone)
    SetMinimumStepLength = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_SetMinimumStepLength)
    GetMinimumStepLength = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_GetMinimumStepLength)
    SetRelaxationFactor = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_SetRelaxationFactor)
    GetRelaxationFactor = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_GetRelaxationFactor)
    SetGradientMagnitudeTolerance = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_SetGradientMagnitudeTolerance)
    GetGradientMagnitudeTolerance = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_GetGradientMagnitudeTolerance)
    SetCurrentLearningRateRelaxation = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_SetCurrentLearningRateRelaxation)
    GetCurrentLearningRateRelaxation = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_GetCurrentLearningRateRelaxation)
    StartOptimization = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_StartOptimization)
    GetCurrentStepLength = _swig_new_instance_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_GetCurrentStepLength)
    __swig_destroy__ = _itkRegularStepGradientDescentOptimizerv4Python.delete_itkRegularStepGradientDescentOptimizerv4F
    cast = _swig_new_static_method(_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_cast)

    def New(*args, **kargs):
        """New() -> itkRegularStepGradientDescentOptimizerv4F

        Create a new object of the class itkRegularStepGradientDescentOptimizerv4F and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkRegularStepGradientDescentOptimizerv4F.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkRegularStepGradientDescentOptimizerv4F.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkRegularStepGradientDescentOptimizerv4F.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkRegularStepGradientDescentOptimizerv4F in _itkRegularStepGradientDescentOptimizerv4Python:
_itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_swigregister(itkRegularStepGradientDescentOptimizerv4F)
itkRegularStepGradientDescentOptimizerv4F___New_orig__ = _itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F___New_orig__
itkRegularStepGradientDescentOptimizerv4F_cast = _itkRegularStepGradientDescentOptimizerv4Python.itkRegularStepGradientDescentOptimizerv4F_cast



