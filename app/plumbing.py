import os
import sys
import zlib
import hashlib

from app.consts import *

def init(base_dir):
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

def cat_file(digest, print_flag):
    obj_dir = os.path.join('.git', 'objects')
    try:
        blob_path = os.path.join(obj_dir, digest[:2], digest[2:])
    except IndexError:
        print(f"invalid sha-1 digest: {digest}", file=sys.stderr)
        return
    try:
        with open(blob_path, mode="rb") as blob:
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
    except FileNotFoundError:
        print(f"digest doesn't correspond to any git object: {digest}", file=sys.stderr)
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