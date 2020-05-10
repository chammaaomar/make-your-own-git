import binascii
import os
import sys
import functools


def sha_to_path(func):
    """A decorator that turns the sha-1 argument of a plumbing command into
    a filepath, and calls func with the contents from the file

    Arguments:
        func {None function(string, *args)} -- A git plumbing function which
        takes the contents of the file in the git object database and a list
        of flags and returns None

    Returns:
        {string, None} func(digest) -- A wrapper function whose return value
        is a string, or None if an error is encountered

    Handles:
        IndexError: if sha-1 digest is too short
        FileNotFoundError: if the sha-1 digest doesn't correspond to an
            object in the git object database '.git/objects'
        It these handles by printing to sys.stderr
    """

    # use functools to maintain the identity
    # and docstring of the wrapped function.
    @functools.wraps(func)
    def wrapper(digest, *flags):
        obj_dir = os.path.join('.git', 'objects')
        try:
            file_path = os.path.join(obj_dir, digest[:2], digest[2:])
        except IndexError:
            print(f"invalid sha-1 digest: {digest}", file=sys.stderr)
            return
        try:
            with open(file_path, mode="rb") as file:
                data = file.read()
                return func(data, *flags)
        except FileNotFoundError:
            print(f"digest doesn't correspond to any git object: {digest}",
                  file=sys.stderr)
            return

    return wrapper


def format_tree(contents):
    # so we can mutate it in-place
    contents = bytearray(contents)
    for i, char in enumerate(contents):
        if char == 0:
            # followed by 20-char SHA-1
            contents[i] = ord(" ")
            contents[i+1:i+21] = binascii.b2a_hex(contents[i+1:i+21])
            contents.insert(i + 41, ord('\n'))
    formatted = []
    for line in contents.split(b"\n"):
        if not line:
            continue
        perm, name, digest = line.split(b" ")
        if perm == b"40000":
            _type = b"tree"
        else:
            _type = b"blob"
        # e.g. 100644 blob <digest>    plumbing.py
        formatted.append(perm + b" " + _type + b" " + digest + b"    " + name)
    return b"\n".join(formatted)
