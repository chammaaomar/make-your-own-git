import os
import sys
import functools

def git_object(func):

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
            print(f"digest doesn't correspond to any git object: {digest}", file=sys.stderr)
            return
    
    return wrapper