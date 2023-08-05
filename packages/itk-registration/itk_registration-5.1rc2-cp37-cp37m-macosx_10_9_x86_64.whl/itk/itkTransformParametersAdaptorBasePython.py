# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _itkTransformParametersAdaptorBasePython.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_itkTransformParametersAdaptorBasePython', [dirname(__file__)])
        except ImportError:
            import _itkTransformParametersAdaptorBasePython
            return _itkTransformParametersAdaptorBasePython
        if fp is not None:
            try:
                _mod = imp.load_module('_itkTransformParametersAdaptorBasePython', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _itkTransformParametersAdaptorBasePython = swig_import_helper()
    del swig_import_helper
else:
    import _itkTransformParametersAdaptorBasePython
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
import ITKCommonBasePython
import pyBasePython
import itkArrayPython
import vnl_vectorPython
import vnl_matrixPython
import stdcomplexPython
import itkTransformBasePython
import itkPointPython
import itkVectorPython
import vnl_vector_refPython
import itkFixedArrayPython
import vnl_matrix_fixedPython
import itkSymmetricSecondRankTensorPython
import itkMatrixPython
import itkCovariantVectorPython
import itkVariableLengthVectorPython
import itkDiffusionTensor3DPython
import itkArray2DPython

def itkTransformParametersAdaptorBaseD3_New():
  return itkTransformParametersAdaptorBaseD3.New()


def itkTransformParametersAdaptorBaseF3_New():
  return itkTransformParametersAdaptorBaseF3.New()


def itkTransformParametersAdaptorBaseD2_New():
  return itkTransformParametersAdaptorBaseD2.New()


def itkTransformParametersAdaptorBaseF2_New():
  return itkTransformParametersAdaptorBaseF2.New()

class itkTransformParametersAdaptorBaseD2(ITKCommonBasePython.itkObject):
    """


    Base helper class intended for multi-resolution image registration.

    During multi-resolution image registration, it is often useful to
    expand the number of parameters describing the transform when going
    from one level to the next. For example, in B-spline registration, one
    often wants to increase the mesh size (or, equivalently, the control
    point grid size) for increased flexibility in optimizing the
    transform. This requires the propagation of the current transform
    solution to the next level where the solution is identical but with an
    increase in the number of parameters. This base class and those
    derived classes are meant to handle these types of situations.

    Basic usage will involve the user specifying the required fixed
    parameters, i.e.

    which will adjust the transform based on the new fixed parameters.

    Nick Tustison

    Marius Staring

    C++ includes: itkTransformParametersAdaptorBase.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def SetTransform(self, _arg: 'itkTransformD22', priorityLower: 'void *'=None) -> "void":
        """
        SetTransform(itkTransformParametersAdaptorBaseD2 self, itkTransformD22 _arg, void * priorityLower=None)
        SetTransform(itkTransformParametersAdaptorBaseD2 self, itkTransformD22 _arg)
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_SetTransform(self, _arg, priorityLower)


    def SetRequiredFixedParameters(self, _arg: 'itkOptimizerParametersD') -> "void":
        """
        SetRequiredFixedParameters(itkTransformParametersAdaptorBaseD2 self, itkOptimizerParametersD _arg)

        Set the
        fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_SetRequiredFixedParameters(self, _arg)


    def GetRequiredFixedParameters(self) -> "itkOptimizerParametersD const &":
        """
        GetRequiredFixedParameters(itkTransformParametersAdaptorBaseD2 self) -> itkOptimizerParametersD

        Get the
        fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_GetRequiredFixedParameters(self)


    def AdaptTransformParameters(self) -> "void":
        """
        AdaptTransformParameters(itkTransformParametersAdaptorBaseD2 self)

        Initialize
        the transform using the specified fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_AdaptTransformParameters(self)

    __swig_destroy__ = _itkTransformParametersAdaptorBasePython.delete_itkTransformParametersAdaptorBaseD2

    def cast(obj: 'itkLightObject') -> "itkTransformParametersAdaptorBaseD2 *":
        """cast(itkLightObject obj) -> itkTransformParametersAdaptorBaseD2"""
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkTransformParametersAdaptorBaseD2

        Create a new object of the class itkTransformParametersAdaptorBaseD2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformParametersAdaptorBaseD2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformParametersAdaptorBaseD2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformParametersAdaptorBaseD2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkTransformParametersAdaptorBaseD2.SetTransform = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_SetTransform, None, itkTransformParametersAdaptorBaseD2)
itkTransformParametersAdaptorBaseD2.SetRequiredFixedParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_SetRequiredFixedParameters, None, itkTransformParametersAdaptorBaseD2)
itkTransformParametersAdaptorBaseD2.GetRequiredFixedParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_GetRequiredFixedParameters, None, itkTransformParametersAdaptorBaseD2)
itkTransformParametersAdaptorBaseD2.AdaptTransformParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_AdaptTransformParameters, None, itkTransformParametersAdaptorBaseD2)
itkTransformParametersAdaptorBaseD2_swigregister = _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_swigregister
itkTransformParametersAdaptorBaseD2_swigregister(itkTransformParametersAdaptorBaseD2)

def itkTransformParametersAdaptorBaseD2_cast(obj: 'itkLightObject') -> "itkTransformParametersAdaptorBaseD2 *":
    """itkTransformParametersAdaptorBaseD2_cast(itkLightObject obj) -> itkTransformParametersAdaptorBaseD2"""
    return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD2_cast(obj)

class itkTransformParametersAdaptorBaseD3(ITKCommonBasePython.itkObject):
    """


    Base helper class intended for multi-resolution image registration.

    During multi-resolution image registration, it is often useful to
    expand the number of parameters describing the transform when going
    from one level to the next. For example, in B-spline registration, one
    often wants to increase the mesh size (or, equivalently, the control
    point grid size) for increased flexibility in optimizing the
    transform. This requires the propagation of the current transform
    solution to the next level where the solution is identical but with an
    increase in the number of parameters. This base class and those
    derived classes are meant to handle these types of situations.

    Basic usage will involve the user specifying the required fixed
    parameters, i.e.

    which will adjust the transform based on the new fixed parameters.

    Nick Tustison

    Marius Staring

    C++ includes: itkTransformParametersAdaptorBase.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def SetTransform(self, _arg: 'itkTransformD33', priorityLower: 'void *'=None) -> "void":
        """
        SetTransform(itkTransformParametersAdaptorBaseD3 self, itkTransformD33 _arg, void * priorityLower=None)
        SetTransform(itkTransformParametersAdaptorBaseD3 self, itkTransformD33 _arg)
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_SetTransform(self, _arg, priorityLower)


    def SetRequiredFixedParameters(self, _arg: 'itkOptimizerParametersD') -> "void":
        """
        SetRequiredFixedParameters(itkTransformParametersAdaptorBaseD3 self, itkOptimizerParametersD _arg)

        Set the
        fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_SetRequiredFixedParameters(self, _arg)


    def GetRequiredFixedParameters(self) -> "itkOptimizerParametersD const &":
        """
        GetRequiredFixedParameters(itkTransformParametersAdaptorBaseD3 self) -> itkOptimizerParametersD

        Get the
        fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_GetRequiredFixedParameters(self)


    def AdaptTransformParameters(self) -> "void":
        """
        AdaptTransformParameters(itkTransformParametersAdaptorBaseD3 self)

        Initialize
        the transform using the specified fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_AdaptTransformParameters(self)

    __swig_destroy__ = _itkTransformParametersAdaptorBasePython.delete_itkTransformParametersAdaptorBaseD3

    def cast(obj: 'itkLightObject') -> "itkTransformParametersAdaptorBaseD3 *":
        """cast(itkLightObject obj) -> itkTransformParametersAdaptorBaseD3"""
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkTransformParametersAdaptorBaseD3

        Create a new object of the class itkTransformParametersAdaptorBaseD3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformParametersAdaptorBaseD3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformParametersAdaptorBaseD3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformParametersAdaptorBaseD3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkTransformParametersAdaptorBaseD3.SetTransform = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_SetTransform, None, itkTransformParametersAdaptorBaseD3)
itkTransformParametersAdaptorBaseD3.SetRequiredFixedParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_SetRequiredFixedParameters, None, itkTransformParametersAdaptorBaseD3)
itkTransformParametersAdaptorBaseD3.GetRequiredFixedParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_GetRequiredFixedParameters, None, itkTransformParametersAdaptorBaseD3)
itkTransformParametersAdaptorBaseD3.AdaptTransformParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_AdaptTransformParameters, None, itkTransformParametersAdaptorBaseD3)
itkTransformParametersAdaptorBaseD3_swigregister = _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_swigregister
itkTransformParametersAdaptorBaseD3_swigregister(itkTransformParametersAdaptorBaseD3)

def itkTransformParametersAdaptorBaseD3_cast(obj: 'itkLightObject') -> "itkTransformParametersAdaptorBaseD3 *":
    """itkTransformParametersAdaptorBaseD3_cast(itkLightObject obj) -> itkTransformParametersAdaptorBaseD3"""
    return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseD3_cast(obj)

class itkTransformParametersAdaptorBaseF2(ITKCommonBasePython.itkObject):
    """


    Base helper class intended for multi-resolution image registration.

    During multi-resolution image registration, it is often useful to
    expand the number of parameters describing the transform when going
    from one level to the next. For example, in B-spline registration, one
    often wants to increase the mesh size (or, equivalently, the control
    point grid size) for increased flexibility in optimizing the
    transform. This requires the propagation of the current transform
    solution to the next level where the solution is identical but with an
    increase in the number of parameters. This base class and those
    derived classes are meant to handle these types of situations.

    Basic usage will involve the user specifying the required fixed
    parameters, i.e.

    which will adjust the transform based on the new fixed parameters.

    Nick Tustison

    Marius Staring

    C++ includes: itkTransformParametersAdaptorBase.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def SetTransform(self, _arg: 'itkTransformF22', priorityLower: 'void *'=None) -> "void":
        """
        SetTransform(itkTransformParametersAdaptorBaseF2 self, itkTransformF22 _arg, void * priorityLower=None)
        SetTransform(itkTransformParametersAdaptorBaseF2 self, itkTransformF22 _arg)
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_SetTransform(self, _arg, priorityLower)


    def SetRequiredFixedParameters(self, _arg: 'itkOptimizerParametersD') -> "void":
        """
        SetRequiredFixedParameters(itkTransformParametersAdaptorBaseF2 self, itkOptimizerParametersD _arg)

        Set the
        fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_SetRequiredFixedParameters(self, _arg)


    def GetRequiredFixedParameters(self) -> "itkOptimizerParametersD const &":
        """
        GetRequiredFixedParameters(itkTransformParametersAdaptorBaseF2 self) -> itkOptimizerParametersD

        Get the
        fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_GetRequiredFixedParameters(self)


    def AdaptTransformParameters(self) -> "void":
        """
        AdaptTransformParameters(itkTransformParametersAdaptorBaseF2 self)

        Initialize
        the transform using the specified fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_AdaptTransformParameters(self)

    __swig_destroy__ = _itkTransformParametersAdaptorBasePython.delete_itkTransformParametersAdaptorBaseF2

    def cast(obj: 'itkLightObject') -> "itkTransformParametersAdaptorBaseF2 *":
        """cast(itkLightObject obj) -> itkTransformParametersAdaptorBaseF2"""
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkTransformParametersAdaptorBaseF2

        Create a new object of the class itkTransformParametersAdaptorBaseF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformParametersAdaptorBaseF2.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformParametersAdaptorBaseF2.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformParametersAdaptorBaseF2.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkTransformParametersAdaptorBaseF2.SetTransform = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_SetTransform, None, itkTransformParametersAdaptorBaseF2)
itkTransformParametersAdaptorBaseF2.SetRequiredFixedParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_SetRequiredFixedParameters, None, itkTransformParametersAdaptorBaseF2)
itkTransformParametersAdaptorBaseF2.GetRequiredFixedParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_GetRequiredFixedParameters, None, itkTransformParametersAdaptorBaseF2)
itkTransformParametersAdaptorBaseF2.AdaptTransformParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_AdaptTransformParameters, None, itkTransformParametersAdaptorBaseF2)
itkTransformParametersAdaptorBaseF2_swigregister = _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_swigregister
itkTransformParametersAdaptorBaseF2_swigregister(itkTransformParametersAdaptorBaseF2)

def itkTransformParametersAdaptorBaseF2_cast(obj: 'itkLightObject') -> "itkTransformParametersAdaptorBaseF2 *":
    """itkTransformParametersAdaptorBaseF2_cast(itkLightObject obj) -> itkTransformParametersAdaptorBaseF2"""
    return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF2_cast(obj)

class itkTransformParametersAdaptorBaseF3(ITKCommonBasePython.itkObject):
    """


    Base helper class intended for multi-resolution image registration.

    During multi-resolution image registration, it is often useful to
    expand the number of parameters describing the transform when going
    from one level to the next. For example, in B-spline registration, one
    often wants to increase the mesh size (or, equivalently, the control
    point grid size) for increased flexibility in optimizing the
    transform. This requires the propagation of the current transform
    solution to the next level where the solution is identical but with an
    increase in the number of parameters. This base class and those
    derived classes are meant to handle these types of situations.

    Basic usage will involve the user specifying the required fixed
    parameters, i.e.

    which will adjust the transform based on the new fixed parameters.

    Nick Tustison

    Marius Staring

    C++ includes: itkTransformParametersAdaptorBase.h 
    """

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def SetTransform(self, _arg: 'itkTransformF33', priorityLower: 'void *'=None) -> "void":
        """
        SetTransform(itkTransformParametersAdaptorBaseF3 self, itkTransformF33 _arg, void * priorityLower=None)
        SetTransform(itkTransformParametersAdaptorBaseF3 self, itkTransformF33 _arg)
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_SetTransform(self, _arg, priorityLower)


    def SetRequiredFixedParameters(self, _arg: 'itkOptimizerParametersD') -> "void":
        """
        SetRequiredFixedParameters(itkTransformParametersAdaptorBaseF3 self, itkOptimizerParametersD _arg)

        Set the
        fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_SetRequiredFixedParameters(self, _arg)


    def GetRequiredFixedParameters(self) -> "itkOptimizerParametersD const &":
        """
        GetRequiredFixedParameters(itkTransformParametersAdaptorBaseF3 self) -> itkOptimizerParametersD

        Get the
        fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_GetRequiredFixedParameters(self)


    def AdaptTransformParameters(self) -> "void":
        """
        AdaptTransformParameters(itkTransformParametersAdaptorBaseF3 self)

        Initialize
        the transform using the specified fixed parameters 
        """
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_AdaptTransformParameters(self)

    __swig_destroy__ = _itkTransformParametersAdaptorBasePython.delete_itkTransformParametersAdaptorBaseF3

    def cast(obj: 'itkLightObject') -> "itkTransformParametersAdaptorBaseF3 *":
        """cast(itkLightObject obj) -> itkTransformParametersAdaptorBaseF3"""
        return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkTransformParametersAdaptorBaseF3

        Create a new object of the class itkTransformParametersAdaptorBaseF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkTransformParametersAdaptorBaseF3.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkTransformParametersAdaptorBaseF3.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkTransformParametersAdaptorBaseF3.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkTransformParametersAdaptorBaseF3.SetTransform = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_SetTransform, None, itkTransformParametersAdaptorBaseF3)
itkTransformParametersAdaptorBaseF3.SetRequiredFixedParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_SetRequiredFixedParameters, None, itkTransformParametersAdaptorBaseF3)
itkTransformParametersAdaptorBaseF3.GetRequiredFixedParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_GetRequiredFixedParameters, None, itkTransformParametersAdaptorBaseF3)
itkTransformParametersAdaptorBaseF3.AdaptTransformParameters = new_instancemethod(_itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_AdaptTransformParameters, None, itkTransformParametersAdaptorBaseF3)
itkTransformParametersAdaptorBaseF3_swigregister = _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_swigregister
itkTransformParametersAdaptorBaseF3_swigregister(itkTransformParametersAdaptorBaseF3)

def itkTransformParametersAdaptorBaseF3_cast(obj: 'itkLightObject') -> "itkTransformParametersAdaptorBaseF3 *":
    """itkTransformParametersAdaptorBaseF3_cast(itkLightObject obj) -> itkTransformParametersAdaptorBaseF3"""
    return _itkTransformParametersAdaptorBasePython.itkTransformParametersAdaptorBaseF3_cast(obj)



