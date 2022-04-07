import os
import platform
import site
import sys


def find_env_setting(arg, env_var_name):
    # We check sys.argv for the arg, and os.environ for the env_var_name
    # The argument gets precedence
    if arg in sys.argv:
        return os.path.abspath(sys.argv[sys.argv.index(arg) + 1])

    if os.environ.get(env_var_name):
        return os.path.abspath(os.environ.get(env_var_name))


def prepend_python_path(root_dir, search_paths_dict):
    # root_dir is the root directory which we will search
    # search_paths_dict is a dictionary with "Linux", "Darwin" (Mac),
    # and "Windows" keys, with niladic functions for the values that
    # returns a list of the paths to search. The paths for the current
    # OS will be used.

    # Returns True on success, False on failure

    # Make sure the python lib dir can be found
    python_lib_path = find_python_path(root_dir, search_paths_dict)
    if python_lib_path is None:
        # A warning should be printed already from find_python_path()
        return False

    # Use site.addsitedir() to automatically process .pth files.
    # This also appends the paths to sys.path. We will move the new
    # paths to the front of sys.path.
    prev_length = len(sys.path)
    site.addsitedir(python_lib_path)
    sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]

    return True


def find_python_path(root_dir, search_paths_dict):
    # Returns the python path, or None if it was not found

    if not os.path.exists(root_dir):
        print(f"Warning: path '{root_dir}' does not exist")
        return None

    if platform.system() not in search_paths_dict:
        raise Exception(f"Unhandled system: {platform.system()}")

    paths_to_try = search_paths_dict[platform.system()]()
    found = False
    for path in paths_to_try:
        full_path = os.path.join(root_dir, path)
        if os.path.exists(full_path):
            found = True
            break

    if not found:
        paths_str = "\n".join(paths_to_try)
        print("Warning: python library path could not be found in "
              f"'{root_dir}'. Tried:\n{paths_str}\n")
        return None

    return full_path
