def clear_triggers(server):
    """
    Helper function to remove all triggers.

    :param server: server on which we want to clear the triggers
    :type server: trame_server.core.Server
    """
    names = list(server._triggers.keys())
    for name in names:
        fn = server._triggers.pop(name)
        server._triggers_fn2name.pop(fn)
        print(f"unregister trigger {name}")


def clear_change_listeners(server):
    """
    Helper function to remove all state.change listeners.

    :param server: server on which we want to clear the state.change listeners
    :type server: trame_server.core.Server
    """
    server._change_callbacks.clear()


def remove_change_listeners(server, *names):
    """
    Helper function to remove any listeners for a given set
    of state variable names.

    :param server: server on which we want to clear the state.change listeners
    :type server: trame_server.core.Server

    :param *names: State variable names
    :type *names: str
    """
    for name in names:
        if name in server._change_callbacks:
            server._change_callbacks.pop(name)


def reload(*reload_list):
    """
    Helper function use to reload python modules that were passed as
    arguments.

    :param *reload_list: positional arguments of the modules to reload when the
                        reload button is pressed.
    :type *reload_list: python modules
    """
    for m in reload_list:
        m.__loader__.exec_module(m)
