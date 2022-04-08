# To support python 3.6
def is_ascii(s):
    # return s.isascii()
    return all(ord(c) < 128 for c in s)

def is_dunder(s):
    # Check if this is a double underscore (dunder) name
    return len(s) > 4 and is_ascii(s) and s[:2] == s[-2:] == "__"
