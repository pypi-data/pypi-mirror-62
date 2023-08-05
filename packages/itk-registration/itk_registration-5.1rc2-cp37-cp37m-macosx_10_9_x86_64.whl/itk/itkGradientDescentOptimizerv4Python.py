# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _itkGradientDescentOptimizerv4Python.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_itkGradientDescentOptimizerv4Python', [dirname(__file__)])
        except ImportError:
            import _itkGradientDescentOptimizerv4Python
            return _itkGradientDescentOptimizerv4Python
        if fp is not None:
            try:
                _mod = imp.load_module('_itkGradientDescentOptimizerv4Python', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _itkGradientDescentOptimizerv4Python = swig_import_helper()
    del swig_import_helper
else:
    import _itkGradientDescentOptimizerv4Python
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


import ITKCommonBasePython
import pyBasePython
import itkIndexPython
import itkSizePython
import itkOffsetPython
import itkGradientDescentOptimizerBasev4Python
import itkArrayPython
import vnl_vectorPython
import vnl_matrixPython
import stdcomplexPython
import itkObjectToObjectOptimizerBasePython
import itkOptimizerParameterScalesEstimatorPython
import itkOptimizerParametersPython
import itkObjectToObjectMetricBasePython
import itkSingleValuedCostFunctionv4Python
import itkCostFunctionPython

def itkGradientDescentOptimizerv4TemplateF_New():
  return itkGradientDescentOptimizerv4TemplateF.New()


def itkGradientDescentOptimizerv4TemplateD_New():
  return itkGradientDescentOptimizerv4TemplateD.New()

class itkGradientDescentOptimizerv4TemplateD(itkGradientDescentOptimizerBasev4Python.itkGradientDescentOptimizerBasev4TemplateD):
    """Proxy of C++ itkGradientDescentOptimizerv4TemplateD class."""

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkGradientDescentOptimizerv4TemplateD_Pointer":
        """__New_orig__() -> itkGradientDescentOptimizerv4TemplateD_Pointer"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkGradientDescentOptimizerv4TemplateD_Pointer":
        """Clone(itkGradientDescentOptimizerv4TemplateD self) -> itkGradientDescentOptimizerv4TemplateD_Pointer"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_Clone(self)


    def SetLearningRate(self, _arg: 'double const') -> "void":
        """SetLearningRate(itkGradientDescentOptimizerv4TemplateD self, double const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetLearningRate(self, _arg)


    def GetLearningRate(self) -> "double const &":
        """GetLearningRate(itkGradientDescentOptimizerv4TemplateD self) -> double const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetLearningRate(self)


    def SetMaximumStepSizeInPhysicalUnits(self, _arg: 'double const') -> "void":
        """SetMaximumStepSizeInPhysicalUnits(itkGradientDescentOptimizerv4TemplateD self, double const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetMaximumStepSizeInPhysicalUnits(self, _arg)


    def GetMaximumStepSizeInPhysicalUnits(self) -> "double const &":
        """GetMaximumStepSizeInPhysicalUnits(itkGradientDescentOptimizerv4TemplateD self) -> double const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetMaximumStepSizeInPhysicalUnits(self)


    def SetDoEstimateLearningRateAtEachIteration(self, _arg: 'bool const') -> "void":
        """SetDoEstimateLearningRateAtEachIteration(itkGradientDescentOptimizerv4TemplateD self, bool const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetDoEstimateLearningRateAtEachIteration(self, _arg)


    def GetDoEstimateLearningRateAtEachIteration(self) -> "bool const &":
        """GetDoEstimateLearningRateAtEachIteration(itkGradientDescentOptimizerv4TemplateD self) -> bool const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetDoEstimateLearningRateAtEachIteration(self)


    def DoEstimateLearningRateAtEachIterationOn(self) -> "void":
        """DoEstimateLearningRateAtEachIterationOn(itkGradientDescentOptimizerv4TemplateD self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_DoEstimateLearningRateAtEachIterationOn(self)


    def DoEstimateLearningRateAtEachIterationOff(self) -> "void":
        """DoEstimateLearningRateAtEachIterationOff(itkGradientDescentOptimizerv4TemplateD self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_DoEstimateLearningRateAtEachIterationOff(self)


    def SetDoEstimateLearningRateOnce(self, _arg: 'bool const') -> "void":
        """SetDoEstimateLearningRateOnce(itkGradientDescentOptimizerv4TemplateD self, bool const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetDoEstimateLearningRateOnce(self, _arg)


    def GetDoEstimateLearningRateOnce(self) -> "bool const &":
        """GetDoEstimateLearningRateOnce(itkGradientDescentOptimizerv4TemplateD self) -> bool const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetDoEstimateLearningRateOnce(self)


    def DoEstimateLearningRateOnceOn(self) -> "void":
        """DoEstimateLearningRateOnceOn(itkGradientDescentOptimizerv4TemplateD self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_DoEstimateLearningRateOnceOn(self)


    def DoEstimateLearningRateOnceOff(self) -> "void":
        """DoEstimateLearningRateOnceOff(itkGradientDescentOptimizerv4TemplateD self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_DoEstimateLearningRateOnceOff(self)


    def SetMinimumConvergenceValue(self, _arg: 'double const') -> "void":
        """SetMinimumConvergenceValue(itkGradientDescentOptimizerv4TemplateD self, double const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetMinimumConvergenceValue(self, _arg)


    def SetConvergenceWindowSize(self, _arg: 'unsigned long const') -> "void":
        """SetConvergenceWindowSize(itkGradientDescentOptimizerv4TemplateD self, unsigned long const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetConvergenceWindowSize(self, _arg)


    def GetConvergenceValue(self) -> "double const &":
        """GetConvergenceValue(itkGradientDescentOptimizerv4TemplateD self) -> double const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetConvergenceValue(self)


    def SetReturnBestParametersAndValue(self, _arg: 'bool const') -> "void":
        """SetReturnBestParametersAndValue(itkGradientDescentOptimizerv4TemplateD self, bool const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetReturnBestParametersAndValue(self, _arg)


    def GetReturnBestParametersAndValue(self) -> "bool const &":
        """GetReturnBestParametersAndValue(itkGradientDescentOptimizerv4TemplateD self) -> bool const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetReturnBestParametersAndValue(self)


    def ReturnBestParametersAndValueOn(self) -> "void":
        """ReturnBestParametersAndValueOn(itkGradientDescentOptimizerv4TemplateD self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_ReturnBestParametersAndValueOn(self)


    def ReturnBestParametersAndValueOff(self) -> "void":
        """ReturnBestParametersAndValueOff(itkGradientDescentOptimizerv4TemplateD self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_ReturnBestParametersAndValueOff(self)


    def StartOptimization(self, doOnlyInitialization: 'bool'=False) -> "void":
        """
        StartOptimization(itkGradientDescentOptimizerv4TemplateD self, bool doOnlyInitialization=False)
        StartOptimization(itkGradientDescentOptimizerv4TemplateD self)
        """
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_StartOptimization(self, doOnlyInitialization)


    def EstimateLearningRate(self) -> "void":
        """EstimateLearningRate(itkGradientDescentOptimizerv4TemplateD self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_EstimateLearningRate(self)

    __swig_destroy__ = _itkGradientDescentOptimizerv4Python.delete_itkGradientDescentOptimizerv4TemplateD

    def cast(obj: 'itkLightObject') -> "itkGradientDescentOptimizerv4TemplateD *":
        """cast(itkLightObject obj) -> itkGradientDescentOptimizerv4TemplateD"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkGradientDescentOptimizerv4TemplateD

        Create a new object of the class itkGradientDescentOptimizerv4TemplateD and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkGradientDescentOptimizerv4TemplateD.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkGradientDescentOptimizerv4TemplateD.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkGradientDescentOptimizerv4TemplateD.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkGradientDescentOptimizerv4TemplateD.Clone = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_Clone, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.SetLearningRate = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetLearningRate, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.GetLearningRate = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetLearningRate, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.SetMaximumStepSizeInPhysicalUnits = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetMaximumStepSizeInPhysicalUnits, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.GetMaximumStepSizeInPhysicalUnits = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetMaximumStepSizeInPhysicalUnits, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.SetDoEstimateLearningRateAtEachIteration = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetDoEstimateLearningRateAtEachIteration, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.GetDoEstimateLearningRateAtEachIteration = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetDoEstimateLearningRateAtEachIteration, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.DoEstimateLearningRateAtEachIterationOn = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_DoEstimateLearningRateAtEachIterationOn, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.DoEstimateLearningRateAtEachIterationOff = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_DoEstimateLearningRateAtEachIterationOff, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.SetDoEstimateLearningRateOnce = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetDoEstimateLearningRateOnce, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.GetDoEstimateLearningRateOnce = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetDoEstimateLearningRateOnce, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.DoEstimateLearningRateOnceOn = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_DoEstimateLearningRateOnceOn, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.DoEstimateLearningRateOnceOff = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_DoEstimateLearningRateOnceOff, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.SetMinimumConvergenceValue = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetMinimumConvergenceValue, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.SetConvergenceWindowSize = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetConvergenceWindowSize, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.GetConvergenceValue = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetConvergenceValue, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.SetReturnBestParametersAndValue = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_SetReturnBestParametersAndValue, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.GetReturnBestParametersAndValue = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_GetReturnBestParametersAndValue, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.ReturnBestParametersAndValueOn = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_ReturnBestParametersAndValueOn, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.ReturnBestParametersAndValueOff = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_ReturnBestParametersAndValueOff, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.StartOptimization = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_StartOptimization, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD.EstimateLearningRate = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_EstimateLearningRate, None, itkGradientDescentOptimizerv4TemplateD)
itkGradientDescentOptimizerv4TemplateD_swigregister = _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_swigregister
itkGradientDescentOptimizerv4TemplateD_swigregister(itkGradientDescentOptimizerv4TemplateD)

def itkGradientDescentOptimizerv4TemplateD___New_orig__() -> "itkGradientDescentOptimizerv4TemplateD_Pointer":
    """itkGradientDescentOptimizerv4TemplateD___New_orig__() -> itkGradientDescentOptimizerv4TemplateD_Pointer"""
    return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD___New_orig__()

def itkGradientDescentOptimizerv4TemplateD_cast(obj: 'itkLightObject') -> "itkGradientDescentOptimizerv4TemplateD *":
    """itkGradientDescentOptimizerv4TemplateD_cast(itkLightObject obj) -> itkGradientDescentOptimizerv4TemplateD"""
    return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateD_cast(obj)

class itkGradientDescentOptimizerv4TemplateF(itkGradientDescentOptimizerBasev4Python.itkGradientDescentOptimizerBasev4TemplateF):
    """Proxy of C++ itkGradientDescentOptimizerv4TemplateF class."""

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkGradientDescentOptimizerv4TemplateF_Pointer":
        """__New_orig__() -> itkGradientDescentOptimizerv4TemplateF_Pointer"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkGradientDescentOptimizerv4TemplateF_Pointer":
        """Clone(itkGradientDescentOptimizerv4TemplateF self) -> itkGradientDescentOptimizerv4TemplateF_Pointer"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_Clone(self)


    def SetLearningRate(self, _arg: 'float const') -> "void":
        """SetLearningRate(itkGradientDescentOptimizerv4TemplateF self, float const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetLearningRate(self, _arg)


    def GetLearningRate(self) -> "float const &":
        """GetLearningRate(itkGradientDescentOptimizerv4TemplateF self) -> float const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetLearningRate(self)


    def SetMaximumStepSizeInPhysicalUnits(self, _arg: 'float const') -> "void":
        """SetMaximumStepSizeInPhysicalUnits(itkGradientDescentOptimizerv4TemplateF self, float const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetMaximumStepSizeInPhysicalUnits(self, _arg)


    def GetMaximumStepSizeInPhysicalUnits(self) -> "float const &":
        """GetMaximumStepSizeInPhysicalUnits(itkGradientDescentOptimizerv4TemplateF self) -> float const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetMaximumStepSizeInPhysicalUnits(self)


    def SetDoEstimateLearningRateAtEachIteration(self, _arg: 'bool const') -> "void":
        """SetDoEstimateLearningRateAtEachIteration(itkGradientDescentOptimizerv4TemplateF self, bool const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetDoEstimateLearningRateAtEachIteration(self, _arg)


    def GetDoEstimateLearningRateAtEachIteration(self) -> "bool const &":
        """GetDoEstimateLearningRateAtEachIteration(itkGradientDescentOptimizerv4TemplateF self) -> bool const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetDoEstimateLearningRateAtEachIteration(self)


    def DoEstimateLearningRateAtEachIterationOn(self) -> "void":
        """DoEstimateLearningRateAtEachIterationOn(itkGradientDescentOptimizerv4TemplateF self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_DoEstimateLearningRateAtEachIterationOn(self)


    def DoEstimateLearningRateAtEachIterationOff(self) -> "void":
        """DoEstimateLearningRateAtEachIterationOff(itkGradientDescentOptimizerv4TemplateF self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_DoEstimateLearningRateAtEachIterationOff(self)


    def SetDoEstimateLearningRateOnce(self, _arg: 'bool const') -> "void":
        """SetDoEstimateLearningRateOnce(itkGradientDescentOptimizerv4TemplateF self, bool const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetDoEstimateLearningRateOnce(self, _arg)


    def GetDoEstimateLearningRateOnce(self) -> "bool const &":
        """GetDoEstimateLearningRateOnce(itkGradientDescentOptimizerv4TemplateF self) -> bool const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetDoEstimateLearningRateOnce(self)


    def DoEstimateLearningRateOnceOn(self) -> "void":
        """DoEstimateLearningRateOnceOn(itkGradientDescentOptimizerv4TemplateF self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_DoEstimateLearningRateOnceOn(self)


    def DoEstimateLearningRateOnceOff(self) -> "void":
        """DoEstimateLearningRateOnceOff(itkGradientDescentOptimizerv4TemplateF self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_DoEstimateLearningRateOnceOff(self)


    def SetMinimumConvergenceValue(self, _arg: 'float const') -> "void":
        """SetMinimumConvergenceValue(itkGradientDescentOptimizerv4TemplateF self, float const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetMinimumConvergenceValue(self, _arg)


    def SetConvergenceWindowSize(self, _arg: 'unsigned long const') -> "void":
        """SetConvergenceWindowSize(itkGradientDescentOptimizerv4TemplateF self, unsigned long const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetConvergenceWindowSize(self, _arg)


    def GetConvergenceValue(self) -> "float const &":
        """GetConvergenceValue(itkGradientDescentOptimizerv4TemplateF self) -> float const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetConvergenceValue(self)


    def SetReturnBestParametersAndValue(self, _arg: 'bool const') -> "void":
        """SetReturnBestParametersAndValue(itkGradientDescentOptimizerv4TemplateF self, bool const _arg)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetReturnBestParametersAndValue(self, _arg)


    def GetReturnBestParametersAndValue(self) -> "bool const &":
        """GetReturnBestParametersAndValue(itkGradientDescentOptimizerv4TemplateF self) -> bool const &"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetReturnBestParametersAndValue(self)


    def ReturnBestParametersAndValueOn(self) -> "void":
        """ReturnBestParametersAndValueOn(itkGradientDescentOptimizerv4TemplateF self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_ReturnBestParametersAndValueOn(self)


    def ReturnBestParametersAndValueOff(self) -> "void":
        """ReturnBestParametersAndValueOff(itkGradientDescentOptimizerv4TemplateF self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_ReturnBestParametersAndValueOff(self)


    def StartOptimization(self, doOnlyInitialization: 'bool'=False) -> "void":
        """
        StartOptimization(itkGradientDescentOptimizerv4TemplateF self, bool doOnlyInitialization=False)
        StartOptimization(itkGradientDescentOptimizerv4TemplateF self)
        """
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_StartOptimization(self, doOnlyInitialization)


    def EstimateLearningRate(self) -> "void":
        """EstimateLearningRate(itkGradientDescentOptimizerv4TemplateF self)"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_EstimateLearningRate(self)

    __swig_destroy__ = _itkGradientDescentOptimizerv4Python.delete_itkGradientDescentOptimizerv4TemplateF

    def cast(obj: 'itkLightObject') -> "itkGradientDescentOptimizerv4TemplateF *":
        """cast(itkLightObject obj) -> itkGradientDescentOptimizerv4TemplateF"""
        return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkGradientDescentOptimizerv4TemplateF

        Create a new object of the class itkGradientDescentOptimizerv4TemplateF and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkGradientDescentOptimizerv4TemplateF.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkGradientDescentOptimizerv4TemplateF.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkGradientDescentOptimizerv4TemplateF.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkGradientDescentOptimizerv4TemplateF.Clone = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_Clone, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.SetLearningRate = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetLearningRate, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.GetLearningRate = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetLearningRate, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.SetMaximumStepSizeInPhysicalUnits = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetMaximumStepSizeInPhysicalUnits, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.GetMaximumStepSizeInPhysicalUnits = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetMaximumStepSizeInPhysicalUnits, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.SetDoEstimateLearningRateAtEachIteration = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetDoEstimateLearningRateAtEachIteration, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.GetDoEstimateLearningRateAtEachIteration = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetDoEstimateLearningRateAtEachIteration, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.DoEstimateLearningRateAtEachIterationOn = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_DoEstimateLearningRateAtEachIterationOn, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.DoEstimateLearningRateAtEachIterationOff = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_DoEstimateLearningRateAtEachIterationOff, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.SetDoEstimateLearningRateOnce = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetDoEstimateLearningRateOnce, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.GetDoEstimateLearningRateOnce = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetDoEstimateLearningRateOnce, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.DoEstimateLearningRateOnceOn = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_DoEstimateLearningRateOnceOn, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.DoEstimateLearningRateOnceOff = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_DoEstimateLearningRateOnceOff, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.SetMinimumConvergenceValue = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetMinimumConvergenceValue, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.SetConvergenceWindowSize = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetConvergenceWindowSize, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.GetConvergenceValue = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetConvergenceValue, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.SetReturnBestParametersAndValue = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_SetReturnBestParametersAndValue, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.GetReturnBestParametersAndValue = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_GetReturnBestParametersAndValue, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.ReturnBestParametersAndValueOn = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_ReturnBestParametersAndValueOn, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.ReturnBestParametersAndValueOff = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_ReturnBestParametersAndValueOff, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.StartOptimization = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_StartOptimization, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF.EstimateLearningRate = new_instancemethod(_itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_EstimateLearningRate, None, itkGradientDescentOptimizerv4TemplateF)
itkGradientDescentOptimizerv4TemplateF_swigregister = _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_swigregister
itkGradientDescentOptimizerv4TemplateF_swigregister(itkGradientDescentOptimizerv4TemplateF)

def itkGradientDescentOptimizerv4TemplateF___New_orig__() -> "itkGradientDescentOptimizerv4TemplateF_Pointer":
    """itkGradientDescentOptimizerv4TemplateF___New_orig__() -> itkGradientDescentOptimizerv4TemplateF_Pointer"""
    return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF___New_orig__()

def itkGradientDescentOptimizerv4TemplateF_cast(obj: 'itkLightObject') -> "itkGradientDescentOptimizerv4TemplateF *":
    """itkGradientDescentOptimizerv4TemplateF_cast(itkLightObject obj) -> itkGradientDescentOptimizerv4TemplateF"""
    return _itkGradientDescentOptimizerv4Python.itkGradientDescentOptimizerv4TemplateF_cast(obj)



