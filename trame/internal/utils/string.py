def is_dunder(s):
    # Check if this is a double underscore (dunder) name
    return len(s) > 4 and s.isascii() and s[:2] == s[-2:] == "__"
