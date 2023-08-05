# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _itkObjectToObjectMetricBasePython.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_itkObjectToObjectMetricBasePython', [dirname(__file__)])
        except ImportError:
            import _itkObjectToObjectMetricBasePython
            return _itkObjectToObjectMetricBasePython
        if fp is not None:
            try:
                _mod = imp.load_module('_itkObjectToObjectMetricBasePython', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _itkObjectToObjectMetricBasePython = swig_import_helper()
    del swig_import_helper
else:
    import _itkObjectToObjectMetricBasePython
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


import itkOptimizerParametersPython
import vnl_vectorPython
import stdcomplexPython
import pyBasePython
import vnl_matrixPython
import ITKCommonBasePython
import itkArrayPython
import itkSingleValuedCostFunctionv4Python
import itkCostFunctionPython

def itkObjectToObjectMetricBaseTemplateF_New():
  return itkObjectToObjectMetricBaseTemplateF.New()


def itkObjectToObjectMetricBaseTemplateD_New():
  return itkObjectToObjectMetricBaseTemplateD.New()

class itkObjectToObjectMetricBaseTemplateD(itkSingleValuedCostFunctionv4Python.itkSingleValuedCostFunctionv4TemplateD):
    """Proxy of C++ itkObjectToObjectMetricBaseTemplateD class."""

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def SetFixedObject(self, _arg: 'itkObject') -> "void":
        """SetFixedObject(itkObjectToObjectMetricBaseTemplateD self, itkObject _arg)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_SetFixedObject(self, _arg)


    def GetFixedObject(self) -> "itkObject const *":
        """GetFixedObject(itkObjectToObjectMetricBaseTemplateD self) -> itkObject"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetFixedObject(self)


    def SetMovingObject(self, _arg: 'itkObject') -> "void":
        """SetMovingObject(itkObjectToObjectMetricBaseTemplateD self, itkObject _arg)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_SetMovingObject(self, _arg)


    def GetMovingObject(self) -> "itkObject const *":
        """GetMovingObject(itkObjectToObjectMetricBaseTemplateD self) -> itkObject"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetMovingObject(self)


    def SetGradientSource(self, _arg: 'itkObjectToObjectMetricBaseTemplateEnums::GradientSource const') -> "void":
        """SetGradientSource(itkObjectToObjectMetricBaseTemplateD self, itkObjectToObjectMetricBaseTemplateEnums::GradientSource const _arg)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_SetGradientSource(self, _arg)


    def GetGradientSource(self) -> "itkObjectToObjectMetricBaseTemplateEnums::GradientSource":
        """GetGradientSource(itkObjectToObjectMetricBaseTemplateD self) -> itkObjectToObjectMetricBaseTemplateEnums::GradientSource"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetGradientSource(self)


    def GetGradientSourceIncludesFixed(self) -> "bool":
        """GetGradientSourceIncludesFixed(itkObjectToObjectMetricBaseTemplateD self) -> bool"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetGradientSourceIncludesFixed(self)


    def GetGradientSourceIncludesMoving(self) -> "bool":
        """GetGradientSourceIncludesMoving(itkObjectToObjectMetricBaseTemplateD self) -> bool"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetGradientSourceIncludesMoving(self)


    def Initialize(self) -> "void":
        """Initialize(itkObjectToObjectMetricBaseTemplateD self)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_Initialize(self)


    def GetDerivative(self, arg0: 'itkArrayD') -> "void":
        """GetDerivative(itkObjectToObjectMetricBaseTemplateD self, itkArrayD arg0)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetDerivative(self, arg0)


    def GetNumberOfLocalParameters(self) -> "unsigned int":
        """GetNumberOfLocalParameters(itkObjectToObjectMetricBaseTemplateD self) -> unsigned int"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetNumberOfLocalParameters(self)


    def SetParameters(self, params: 'itkOptimizerParametersD') -> "void":
        """SetParameters(itkObjectToObjectMetricBaseTemplateD self, itkOptimizerParametersD params)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_SetParameters(self, params)


    def GetParameters(self) -> "itkOptimizerParametersD const &":
        """GetParameters(itkObjectToObjectMetricBaseTemplateD self) -> itkOptimizerParametersD"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetParameters(self)


    def HasLocalSupport(self) -> "bool":
        """HasLocalSupport(itkObjectToObjectMetricBaseTemplateD self) -> bool"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_HasLocalSupport(self)


    def UpdateTransformParameters(self, *args) -> "void":
        """
        UpdateTransformParameters(itkObjectToObjectMetricBaseTemplateD self, itkArrayD derivative, double factor)
        UpdateTransformParameters(itkObjectToObjectMetricBaseTemplateD self, itkArrayD derivative)
        """
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_UpdateTransformParameters(self, *args)


    def GetCurrentValue(self) -> "double":
        """GetCurrentValue(itkObjectToObjectMetricBaseTemplateD self) -> double"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetCurrentValue(self)


    def GetMetricCategory(self) -> "itkObjectToObjectMetricBaseTemplateEnums::MetricCategory":
        """GetMetricCategory(itkObjectToObjectMetricBaseTemplateD self) -> itkObjectToObjectMetricBaseTemplateEnums::MetricCategory"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetMetricCategory(self)

    __swig_destroy__ = _itkObjectToObjectMetricBasePython.delete_itkObjectToObjectMetricBaseTemplateD

    def cast(obj: 'itkLightObject') -> "itkObjectToObjectMetricBaseTemplateD *":
        """cast(itkLightObject obj) -> itkObjectToObjectMetricBaseTemplateD"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkObjectToObjectMetricBaseTemplateD

        Create a new object of the class itkObjectToObjectMetricBaseTemplateD and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkObjectToObjectMetricBaseTemplateD.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkObjectToObjectMetricBaseTemplateD.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkObjectToObjectMetricBaseTemplateD.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkObjectToObjectMetricBaseTemplateD.SetFixedObject = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_SetFixedObject, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetFixedObject = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetFixedObject, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.SetMovingObject = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_SetMovingObject, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetMovingObject = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetMovingObject, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.SetGradientSource = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_SetGradientSource, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetGradientSource = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetGradientSource, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetGradientSourceIncludesFixed = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetGradientSourceIncludesFixed, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetGradientSourceIncludesMoving = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetGradientSourceIncludesMoving, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.Initialize = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_Initialize, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetDerivative = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetDerivative, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetNumberOfLocalParameters = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetNumberOfLocalParameters, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.SetParameters = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_SetParameters, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetParameters = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetParameters, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.HasLocalSupport = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_HasLocalSupport, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.UpdateTransformParameters = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_UpdateTransformParameters, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetCurrentValue = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetCurrentValue, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD.GetMetricCategory = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_GetMetricCategory, None, itkObjectToObjectMetricBaseTemplateD)
itkObjectToObjectMetricBaseTemplateD_swigregister = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_swigregister
itkObjectToObjectMetricBaseTemplateD_swigregister(itkObjectToObjectMetricBaseTemplateD)

def itkObjectToObjectMetricBaseTemplateD_cast(obj: 'itkLightObject') -> "itkObjectToObjectMetricBaseTemplateD *":
    """itkObjectToObjectMetricBaseTemplateD_cast(itkLightObject obj) -> itkObjectToObjectMetricBaseTemplateD"""
    return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateD_cast(obj)

class itkObjectToObjectMetricBaseTemplateEnums(object):
    """Proxy of C++ itkObjectToObjectMetricBaseTemplateEnums class."""

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    GradientSource_GRADIENT_SOURCE_FIXED = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_GradientSource_GRADIENT_SOURCE_FIXED
    GradientSource_GRADIENT_SOURCE_MOVING = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_GradientSource_GRADIENT_SOURCE_MOVING
    GradientSource_GRADIENT_SOURCE_BOTH = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_GradientSource_GRADIENT_SOURCE_BOTH
    MetricCategory_UNKNOWN_METRIC = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_MetricCategory_UNKNOWN_METRIC
    MetricCategory_OBJECT_METRIC = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_MetricCategory_OBJECT_METRIC
    MetricCategory_IMAGE_METRIC = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_MetricCategory_IMAGE_METRIC
    MetricCategory_POINT_SET_METRIC = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_MetricCategory_POINT_SET_METRIC
    MetricCategory_MULTI_METRIC = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_MetricCategory_MULTI_METRIC

    def __init__(self, *args):
        """
        __init__(itkObjectToObjectMetricBaseTemplateEnums self) -> itkObjectToObjectMetricBaseTemplateEnums
        __init__(itkObjectToObjectMetricBaseTemplateEnums self, itkObjectToObjectMetricBaseTemplateEnums arg0) -> itkObjectToObjectMetricBaseTemplateEnums
        """
        _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_swiginit(self, _itkObjectToObjectMetricBasePython.new_itkObjectToObjectMetricBaseTemplateEnums(*args))
    __swig_destroy__ = _itkObjectToObjectMetricBasePython.delete_itkObjectToObjectMetricBaseTemplateEnums
itkObjectToObjectMetricBaseTemplateEnums_swigregister = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateEnums_swigregister
itkObjectToObjectMetricBaseTemplateEnums_swigregister(itkObjectToObjectMetricBaseTemplateEnums)

class itkObjectToObjectMetricBaseTemplateF(itkSingleValuedCostFunctionv4Python.itkSingleValuedCostFunctionv4TemplateF):
    """Proxy of C++ itkObjectToObjectMetricBaseTemplateF class."""

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def SetFixedObject(self, _arg: 'itkObject') -> "void":
        """SetFixedObject(itkObjectToObjectMetricBaseTemplateF self, itkObject _arg)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_SetFixedObject(self, _arg)


    def GetFixedObject(self) -> "itkObject const *":
        """GetFixedObject(itkObjectToObjectMetricBaseTemplateF self) -> itkObject"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetFixedObject(self)


    def SetMovingObject(self, _arg: 'itkObject') -> "void":
        """SetMovingObject(itkObjectToObjectMetricBaseTemplateF self, itkObject _arg)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_SetMovingObject(self, _arg)


    def GetMovingObject(self) -> "itkObject const *":
        """GetMovingObject(itkObjectToObjectMetricBaseTemplateF self) -> itkObject"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetMovingObject(self)


    def SetGradientSource(self, _arg: 'itkObjectToObjectMetricBaseTemplateEnums::GradientSource const') -> "void":
        """SetGradientSource(itkObjectToObjectMetricBaseTemplateF self, itkObjectToObjectMetricBaseTemplateEnums::GradientSource const _arg)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_SetGradientSource(self, _arg)


    def GetGradientSource(self) -> "itkObjectToObjectMetricBaseTemplateEnums::GradientSource":
        """GetGradientSource(itkObjectToObjectMetricBaseTemplateF self) -> itkObjectToObjectMetricBaseTemplateEnums::GradientSource"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetGradientSource(self)


    def GetGradientSourceIncludesFixed(self) -> "bool":
        """GetGradientSourceIncludesFixed(itkObjectToObjectMetricBaseTemplateF self) -> bool"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetGradientSourceIncludesFixed(self)


    def GetGradientSourceIncludesMoving(self) -> "bool":
        """GetGradientSourceIncludesMoving(itkObjectToObjectMetricBaseTemplateF self) -> bool"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetGradientSourceIncludesMoving(self)


    def Initialize(self) -> "void":
        """Initialize(itkObjectToObjectMetricBaseTemplateF self)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_Initialize(self)


    def GetDerivative(self, arg0: 'itkArrayF') -> "void":
        """GetDerivative(itkObjectToObjectMetricBaseTemplateF self, itkArrayF arg0)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetDerivative(self, arg0)


    def GetNumberOfLocalParameters(self) -> "unsigned int":
        """GetNumberOfLocalParameters(itkObjectToObjectMetricBaseTemplateF self) -> unsigned int"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetNumberOfLocalParameters(self)


    def SetParameters(self, params: 'itkOptimizerParametersF') -> "void":
        """SetParameters(itkObjectToObjectMetricBaseTemplateF self, itkOptimizerParametersF params)"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_SetParameters(self, params)


    def GetParameters(self) -> "itkOptimizerParametersF const &":
        """GetParameters(itkObjectToObjectMetricBaseTemplateF self) -> itkOptimizerParametersF"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetParameters(self)


    def HasLocalSupport(self) -> "bool":
        """HasLocalSupport(itkObjectToObjectMetricBaseTemplateF self) -> bool"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_HasLocalSupport(self)


    def UpdateTransformParameters(self, *args) -> "void":
        """
        UpdateTransformParameters(itkObjectToObjectMetricBaseTemplateF self, itkArrayF derivative, float factor)
        UpdateTransformParameters(itkObjectToObjectMetricBaseTemplateF self, itkArrayF derivative)
        """
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_UpdateTransformParameters(self, *args)


    def GetCurrentValue(self) -> "float":
        """GetCurrentValue(itkObjectToObjectMetricBaseTemplateF self) -> float"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetCurrentValue(self)


    def GetMetricCategory(self) -> "itkObjectToObjectMetricBaseTemplateEnums::MetricCategory":
        """GetMetricCategory(itkObjectToObjectMetricBaseTemplateF self) -> itkObjectToObjectMetricBaseTemplateEnums::MetricCategory"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetMetricCategory(self)

    __swig_destroy__ = _itkObjectToObjectMetricBasePython.delete_itkObjectToObjectMetricBaseTemplateF

    def cast(obj: 'itkLightObject') -> "itkObjectToObjectMetricBaseTemplateF *":
        """cast(itkLightObject obj) -> itkObjectToObjectMetricBaseTemplateF"""
        return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkObjectToObjectMetricBaseTemplateF

        Create a new object of the class itkObjectToObjectMetricBaseTemplateF and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkObjectToObjectMetricBaseTemplateF.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkObjectToObjectMetricBaseTemplateF.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkObjectToObjectMetricBaseTemplateF.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkObjectToObjectMetricBaseTemplateF.SetFixedObject = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_SetFixedObject, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetFixedObject = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetFixedObject, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.SetMovingObject = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_SetMovingObject, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetMovingObject = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetMovingObject, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.SetGradientSource = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_SetGradientSource, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetGradientSource = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetGradientSource, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetGradientSourceIncludesFixed = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetGradientSourceIncludesFixed, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetGradientSourceIncludesMoving = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetGradientSourceIncludesMoving, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.Initialize = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_Initialize, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetDerivative = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetDerivative, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetNumberOfLocalParameters = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetNumberOfLocalParameters, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.SetParameters = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_SetParameters, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetParameters = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetParameters, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.HasLocalSupport = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_HasLocalSupport, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.UpdateTransformParameters = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_UpdateTransformParameters, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetCurrentValue = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetCurrentValue, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF.GetMetricCategory = new_instancemethod(_itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_GetMetricCategory, None, itkObjectToObjectMetricBaseTemplateF)
itkObjectToObjectMetricBaseTemplateF_swigregister = _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_swigregister
itkObjectToObjectMetricBaseTemplateF_swigregister(itkObjectToObjectMetricBaseTemplateF)

def itkObjectToObjectMetricBaseTemplateF_cast(obj: 'itkLightObject') -> "itkObjectToObjectMetricBaseTemplateF *":
    """itkObjectToObjectMetricBaseTemplateF_cast(itkLightObject obj) -> itkObjectToObjectMetricBaseTemplateF"""
    return _itkObjectToObjectMetricBasePython.itkObjectToObjectMetricBaseTemplateF_cast(obj)



