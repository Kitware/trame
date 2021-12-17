from trame.internal.utils import is_dunder
from .decorators import trigger


class Controller:
    """Controller acts as a container for function proxies

    It allows functions to be passed around that are not yet defined,
    and can be defined or re-defined later. For example:

    >>> f = ctrl.hello_func  # function is currently undefined
    >>> ctrl.hello_func = lambda: print("Hello, world!")
    >>> f()
    Hello, world!

    >>> ctrl.hello_func = lambda: print("Hello again!")
    >>> f()
    Hello again!
    """
    def __init__(self):
        super().__setattr__('_func_dict', {})

    def __getattr__(self, name):
        if is_dunder(name):
            return super().__getattr__(name)

        if name not in self._func_dict:
            self._func_dict[name] = ControllerFunction(name)

        # The ControllerFunction object is callable, but we will return the
        # __call__ method for greater compatibility in case a function is
        # required.
        return self._func_dict[name].__call__

    def __setattr__(self, name, func):
        # Do not allow pre-existing attributes, such as `trigger`, to be
        # re-defined.
        if name in self.__dict__ or name in Controller.__dict__:
            msg = (
                f"'{name}' is a special attribute on Controller that cannot "
                "be re-assigned"
            )
            raise Exception(msg)

        if name in self._func_dict:
            self._func_dict[name].func = func
        else:
            self._func_dict[name] = ControllerFunction(name, func)

    # Allow the trigger decorator to be accessed via @controller.trigger
    trigger = staticmethod(trigger)


class ControllerFunction:
    """Controller functions are callable function proxy objects

    Any calls are forwarded to the internal function, which may be
    undefined or dynamically changed. If a call is made when the
    internal function is undefined, a FunctionNotImplementedError is
    raised.
    """
    def __init__(self, name, func=None):
        # The name is needed to provide more helpful information upon
        # a FunctionNotImplementedError exception.
        self.name = name
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.func is None:
            raise FunctionNotImplementedError(self.name)

        return self.func(*args, **kwargs)


class FunctionNotImplementedError(Exception):
    pass
