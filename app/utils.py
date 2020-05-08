import os
import sys
import functools


def sha_to_path(func):
    """A decorator that turns the sha-1 argument of a plumbing command into
    a filepath, and handles errors from an invalid sha-1 if non-existant
    file or sha-1 too short.

    Arguments:
        func {None function(string, *args)} -- A git plumbing function which
        takes a filepath to the object in the git object database and a list
        of flags and returns None

    Returns:
        None -- its action is side-effect only: writing to stdout or a file.
    """

    # use functools to maintain the identity
    # and docstring of the wrapped function.
    @functools.wraps(func)
    def wrapper(digest, *flags):
        obj_dir = os.path.join('.git', 'objects')
        try:
            obj_path = os.path.join(obj_dir, digest[:2], digest[2:])
        except IndexError:
            print(f"invalid sha-1 digest: {digest}", file=sys.stderr)
            return
        try:
            func(obj_path, *flags)
        except FileNotFoundError:
            print(f"digest doesn't correspond to any git object: {digest}",
                  file=sys.stderr)
            return

    return wrapper
