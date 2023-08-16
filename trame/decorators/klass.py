import inspect
import logging

logger = logging.getLogger(__name__)

# logging.basicConfig(level=logging.DEBUG)


def can_be_decorated(x):
    return inspect.ismethod(x) or inspect.isfunction(x)


class TrameApp:
    """
    Class Decorator for trame application.
    This decorator can be used to automatically register methods to state.change, controller, trigger and life_cycle.
    The parameter are used to define where to fine the server instance within the object and where a namespace for the variable name is stored.


    .. code-block:: python

        @TrameApp()
        class ExampleApp:
            def __init__(self):
                self.server = get_server()

            @change("var_name_1", "var_name_n")
            def on_state_change(**kwargs):
                pass

            @controller.set("hello")
            def hello(**kwargs):
                pass

    """

    def __init__(self, server="server", namespace=""):
        self.server_name = server
        self.namespace_prefix = namespace

    def __call__(self, klass):
        def decorated_constructor(*args, **kwargs):
            logger.debug("Create instance")
            instance = klass(*args, **kwargs)
            logger.debug("Instance created")

            server = getattr(instance, self.server_name)
            prefix = (
                getattr(instance, self.namespace_prefix)
                if self.namespace_prefix
                else ""
            )

            logger.debug(f"{server=} {prefix=}")

            # Look for method decorator
            for k in inspect.getmembers(instance.__class__, can_be_decorated):
                fn = getattr(instance, k[0])

                # Handle @state.change
                if "_trame_state_change" in fn.__dict__:
                    state_change_names = fn.__dict__["_trame_state_change"]
                    logger.debug(
                        f"state.change({[f'{prefix}{v}' for v in state_change_names]})({k[0]})"
                    )
                    server.state.change(*[f"{prefix}{v}" for v in state_change_names])(
                        fn
                    )

                # Handle @trigger
                if "_trame_trigger_names" in fn.__dict__:
                    trigger_names = fn.__dict__["_trame_trigger_names"]
                    for trigger_name in trigger_names:
                        logger.debug(f"trigger({trigger_name})({k[0]})")
                        server.trigger(f"{trigger_name}")(fn)
                        if prefix:
                            logger.debug(f"trigger({prefix}{trigger_name})({k[0]})")
                            server.trigger(f"{prefix}{trigger_name}")(fn)

                # Handle @ctrl.[add, once, add_task, set]
                if "_trame_controller" in fn.__dict__:
                    actions = fn.__dict__["_trame_controller"]
                    for action in actions:
                        name = action.get("name")
                        method = action.get("method")
                        decorate = getattr(server.controller, method)
                        logger.debug(f"ctrl.{method}({name})({k[0]})")
                        decorate(name)(fn)
                        if prefix:
                            logger.debug(f"ctrl.{method}({prefix}{name})({k[0]})")
                            decorate(f"{prefix}{name}")(fn)

            return instance

        return decorated_constructor


def change(*args):
    """Method decorator for state change"""

    def decorate(f):
        if not hasattr(f, "_trame_state_change"):
            f._trame_state_change = []
        f._trame_state_change.extend(args)
        return f

    return decorate


def trigger(*args):
    """Method decorator to assign a trigger name to a function"""

    def decorate(f):
        if not hasattr(f, "_trame_trigger_names"):
            f._trame_trigger_names = []
        f._trame_trigger_names.extend(args)
        return f

    return decorate


def controller_decorator(method):
    def decorator(*args):
        def decorate(f):
            if not hasattr(f, "_trame_controller"):
                f._trame_controller = []
            for name in args:
                f._trame_controller.append(dict(method=method, name=name))
            return f

        return decorate

    return decorator


class Controller:
    """Controller decorators

    .. code-block:: text

        - once
        - add
        - add_task
        - set
    """

    def __init__(self):
        self.once = controller_decorator("once")
        self.add = controller_decorator("add")
        self.add_task = controller_decorator("add_task")
        self.set = controller_decorator("set")


class LifeCycle:
    """Life Cycle decorators

    .. code-block:: text

        - server_start
        - server_bind
        - server_ready
        - client_connected
        - client_exited
        - server_exited
        - server_reload

    """

    def __init__(self):
        self.server_start = controller_decorator("add")("on_server_start")
        self.server_bind = controller_decorator("add")("on_server_bind")
        self.server_ready = controller_decorator("add")("on_server_ready")
        self.client_connected = controller_decorator("add")("on_client_connected")
        self.client_exited = controller_decorator("add")("on_client_exited")
        self.server_exited = controller_decorator("add")("on_server_exited")
        self.server_reload = controller_decorator("add")("on_server_reload")


controller = Controller()
life_cycle = LifeCycle()


__all__ = [
    "TrameApp",
    "change",
    "trigger",
    "controller",
    "life_cycle",
]
