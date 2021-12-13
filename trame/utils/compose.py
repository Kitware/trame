def compose_callbacks(*args):
    def __fn(**kwargs):
        for _fn in args:
            if _fn is None:
                continue
            try:
                _fn(**kwargs)
            except TypeError:
                _fn()

    return __fn
