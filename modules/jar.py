import os
import subprocess


def j_call(*, file: str, args: list = []):
    """ call java (file) (.jar) as a subprocess with arguments (args) """
    if type(file) != str:
        raise TypeError("'file' must be of type str")
    if not (os.path.exists(file) and os.path.isfile(file)):
        raise FileNotFoundError(f"{file} of type 'file' not found")
    if type(args) != list:
        raise TypeError("'args' must be of type list")
    if args != [] and type(args[0]) != str:
        raise TypeError("'args' must be a list of strings")
    child = subprocess.run([
                               'java',
                               '-jar',
                               file,
                           ] + args)
    return child.returncode
