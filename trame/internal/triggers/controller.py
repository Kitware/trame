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

    >>> ctrl.on_data_change.add(lambda: print("Update pipeline!"))
    >>> ctrl.on_data_change.add(lambda: print("Update view!"))
    >>> ctrl.on_data_change.add(lambda: print("Wow that is pretty cool!"))
    >>> ctrl.on_data_change()
    "Update pipeline!"
    "Wow that is pretty cool!"
    "Update view!"
    >>> ctrl.on_data_change.clear(set_only=True) # add, remove, discard, clear
    """

    def __init__(self):
        super().__setattr__("_func_dict", {})

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        self.__setattr__(name, value)

    def __getattr__(self, name):
        if is_dunder(name):
            return super().__getattr__(name)

        if name not in self._func_dict:
            self._func_dict[name] = ControllerFunction(name)

        return self._func_dict[name]

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
        self.funcs = set()

    def __call__(self, *args, **kwargs):
        if self.func is None and len(self.funcs) == 0:
            raise FunctionNotImplementedError(self.name)

        results = list(map(lambda f: f(*args, **kwargs), self.funcs))
        if self.func is not None:
            return self.func(*args, **kwargs)

        return results

    def add(self, func):
        self.funcs.add(func)

    def discard(self, func):
        self.funcs.discard(func)

    def remove(self, func):
        self.funcs.remove(func)

    def clear(self, set_only=False):
        if not set_only:
            self.func = None

        self.funcs.clear()


class FunctionNotImplementedError(Exception):
    pass
