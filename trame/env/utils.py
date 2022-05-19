import os
import platform
import site
import sys
import subprocess


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


def append_path_to_environ(var_name, paths):
    result_paths = []
    current_var_value = os.environ.get(var_name, "")
    sys_path_sepa = ";" if platform.system() == "Windows" else ":"

    if len(current_var_value):
        result_paths.append(current_var_value)

    for path_entry in paths:
        if path_entry not in current_var_value:
            result_paths.append(path_entry)

    if len(result_paths):
        os.environ[var_name] = sys_path_sepa.join(result_paths)


def filter_existing_paths(root_dir, paths_to_try):
    found_paths = []

    for path in paths_to_try:
        full_path = os.path.join(root_dir, path)
        if os.path.exists(full_path):
            found_paths.append(full_path)

    return found_paths


def find_python_path(root_dir, search_paths_dict):
    # Returns the python path, or None if it was not found

    if not os.path.exists(root_dir):
        print(f"Warning: path '{root_dir}' does not exist")
        return None

    if platform.system() not in search_paths_dict:
        raise Exception(f"Unhandled system: {platform.system()}")

    paths_to_try = search_paths_dict[platform.system()]()
    found_paths = filter_existing_paths(root_dir, paths_to_try)

    if len(found_paths) != 1:
        paths_str = "\n".join(paths_to_try)
        print(
            "Warning: python library path could not be found in "
            f"'{root_dir}'. Tried:\n{paths_str}\n"
        )
        return None

    return found_paths[0]


def rerun(base_path, add_path_vars, remove_vars=[]):
    for name, paths in add_path_vars.items():
        resolved_paths = filter_existing_paths(base_path, paths)
        append_path_to_environ(name, resolved_paths)

    clear_environ_variables(*remove_vars)
    rerun_with_new_environ(*list(add_path_vars.keys()))


def rerun_with_new_environ(*var_to_print):
    if not os.environ.get("__IN_TRAME_RERUN") == "YES":
        env = os.environ.copy()
        env["__IN_TRAME_RERUN"] = "YES"

        # Print env info
        if len(var_to_print):
            print("-" * 80)
            print("Re-excuting with following environment variables:")
            for name in var_to_print:
                print(f" - {name}={env.get(name)}")
            print("-" * 80)

        # Re-run the same command with the modified environment
        cmd = [sys.executable] + sys.argv
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, env=env)
        sys.exit()


def clear_environ_variables(*names):
    for var in names:
        if var in os.environ:
            os.environ.pop(var)
