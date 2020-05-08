import os
import sys
import zlib
import hashlib

from app.consts import *
from app.utils import sha_to_path


def init(base_dir):
    """initialize minimal git directory in @base_dir. Currently
    no support for packing or tags.

    Arguments:
        base_dir {string} -- path to directory in which to initialize .git
    """
    git_dir = os.path.join(base_dir, ".git")
    obj_dir = os.path.join(git_dir, "objects")
    ref_dir = os.path.join(git_dir, "refs")
    head_f = os.path.join(git_dir, "HEAD")
    os.makedirs(base_dir, exist_ok=True)
    os.mkdir(git_dir)
    os.mkdir(ref_dir)
    os.mkdir(obj_dir)
    with open(head_f, "w+") as f:
        f.write("ref: refs/heads/master\n")
    print(f"Initialized empty git repository in {git_dir}")


@sha_to_path
def cat_file(obj_path, print_flag):
    with open(obj_path, mode="rb") as blob:
        data = blob.read()
        header, contents = zlib.decompress(data).split(b"\x00")
        _type, size = header.split(b" ")
        if print_flag == P_FL:
            sys.stdout.write(contents.decode("utf-8"))
            return
        if print_flag == S_FL:
            sys.stdout.write(size.decode("utf-8"))
            return
        if print_flag == T_FL:
            sys.stdout.write(_type.decode("utf-8"))
            return


def hash_object(file_path, write):
    try:
        with open(file_path, mode="rb") as file:
            contents = file.read()
            header = f"blob {len(contents)}\x00"
            hasher = hashlib.sha1()
            hasher.update(header.encode("utf-8"))
            hasher.update(contents)
            digest = hasher.hexdigest()
            if write:
                obj_dir = os.path.join('.git', 'objects', digest[:2])
                os.makedirs(obj_dir, exist_ok=True)
                obj_path = os.path.join(obj_dir, digest[2:])
                with open(obj_path, mode="wb+") as out:
                    compressed = zlib.compress(header.encode("utf-8")+contents)
                    out.write(compressed)
            sys.stdout.write(digest)
    except FileNotFoundError:
        print(f"invalid file path: {file_path}", file=sys.stderr)


@sha_to_path
def ls_tree(tree_path, *flags):
    [lsfmt_flag, recur_flag] = flags
    with open(tree_path, mode="rb") as tree:
        data = tree.read()
        content = zlib.decompress(data).split(b"\x00")
        # we want to keep both "tree <tree size in bytes>"
        tokens = [*content[0].split(b" ")]
        tokens += [item.split(b" ")[1]
                   for i, item in enumerate(content) if i > 0 and b" " in item]
        if lsfmt_flag == NAMEONLY_FL:
            name_tokens = [str(t, encoding="utf-8") for t in tokens[2:]]
            print("\n".join(name_tokens))
