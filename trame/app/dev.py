def clear_triggers(server):
    names = list(server._triggers.keys())
    for name in names:
        fn = server._triggers.pop(name)
        server._triggers_fn2name.pop(fn)
        print(f"unregister trigger {name}")


def clear_change_listeners(server):
    server._change_callbacks.clear()


def remove_change_listeners(server, *names):
    for name in names:
        if name in server._change_callbacks:
            server._change_callbacks.pop(name)


def reload(*reload_list):
    """
    Helper function use to reload python modules that were passed as
    arguments.

    :param reload_list: positional arguments of the modules to reload when the
                        reload button is pressed.
    :type reload_list: python modules
    """
    for m in reload_list:
        m.__loader__.exec_module(m)
