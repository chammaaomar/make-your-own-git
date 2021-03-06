import binascii
import time
import hashlib
import os
import sys
import zlib

from app.consts import *
from app.utils import sha_to_path, format_tree


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
def cat_file(data, print_flag):
    """Prints the contents of an object encoded / compressed by
    git hash-object or ./your_git.sh hash-object. It currently expects
    the contents to be of the form "type <size in bytes>\x00contents".
    It only works reliably with blob objects right now, but may work
    with trees.

    Arguments:
        obj_path {string} -- path to object in git object database
        print_flag {int} --
            1: print the contents of the object
            2: print the size in bytes of the object
            3: print the type of the object, e.g. blob
    """
    decompressed = zlib.decompress(data)
    delimiter = decompressed.index(b"\x00")
    header, contents = decompressed[:delimiter], decompressed[delimiter+1:]
    _type, size = header.split(b" ")
    if _type == b'tree':
        contents = format_tree(contents)
    if print_flag == P_FL:
        return contents.decode("utf-8")
    if print_flag == S_FL:
        return size.decode("utf-8")
    if print_flag == T_FL:
        return _type.decode("utf-8")


def hash_object(contents, write, _type="blob"):
    """Produces the content-addressing id at which the object would be stored
    in the git object database

    Arguments:
        contents {bytes} -- File contents as bytes array or bytes string
        write {boolean} -- actually store the object in the git object database.

    The output format is the input formatted expected by git cat-file,
    "type <size in bytes>\x00contents"

    Returns:
        {[string], 0} -- 40-character sha-1 digest
    """
    header = f"{_type} {len(contents)}\x00"
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
    return digest


@sha_to_path
def ls_tree(data, *flags):
    [lsfmt_flag, recur_flag] = flags
    content = zlib.decompress(data).split(b"\x00")
    # we want to keep both "tree <tree size in bytes>"
    tokens = [*content[0].split(b" ")]
    tokens += [item.split(b" ")[-1]
               for i, item in enumerate(content) if i > 0 and b" " in item]
    if recur_flag:
        print("--recursive flag not yet supported", file=sys.stderr)
        return None
    if lsfmt_flag == NAMEONLY_FL:
        name_tokens = [str(t, encoding="utf-8") for t in tokens[2:]]
        return "\n".join(name_tokens)
    else:
        print("Only --name-only flag is currently supported", file=sys.stderr)
        return None


def write_tree(prefix):
    content = []
    root, dirs, files = next(os.walk(prefix))
    gitignore = ['.git', '__pycache__']
    # basic gitignore... needs work
    for term in gitignore:
        if os.path.basename(root) == term:
            return
        if f"/{term}/" in root:
            return
    for _dir in dirs:
        # basic gitignore
        for term in gitignore:
            if term == _dir:
                break
        else:  # no break, i.e. not gitignored
            sub_tree = os.path.join(root, _dir)
            sha1_bin = binascii.a2b_hex(write_tree(sub_tree))
            header = f"40000 {_dir}\0"
            content.append(header.encode("utf-8") + sha1_bin)
    for fname in files:
        fpath = os.path.join(root, fname)
        oct_perm = oct(os.stat(fpath).st_mode)[2:]
        header = f"{oct_perm} {fname}\0"
        with open(fpath, mode="rb") as file:
            file_bytes = file.read()
            sha1_bin = binascii.a2b_hex(hash_object(
                file_bytes, write=True, _type='blob'))
        content.append(header.encode("utf-8") + sha1_bin)

    content.sort(key=lambda line: line.split(b" ")[1].split(b"\0")[0])
    content_bytes = b"".join(content)
    digest = hash_object(content_bytes, True, "tree")

    # SHA-1 is 20 bytes
    return digest


def commit_tree(tree_digest, message, parent_commit=None):
    commit_contents = []
    info = {
        "author": (os.environ.get("AUTHOR_NAME", default="John Doe"),
                   os.environ.get("AUTHOR_EMAIL", default="john.doe@email.com")),
        "commiter": (os.environ.get("COMMITER_NAME", default="John Doe"),
                     os.environ.get("AUTHOR_EMAIL", default="john.doe@email.com"))
    }
    commit_time = int(time.time())
    # gives difference from UTC in hours, accounting for daylight saving
    utc_diff = time.timezone if not time.localtime().tm_isdst else time.altzone
    # in minutes. The minus sign is to produce the correct value
    utc_diff /= (-60 * 60)
    utc_diff *= 100
    parent_content = f"parent {parent_commit}\n" if parent_commit else ""
    commit_contents = [
        f"tree {tree_digest}\n",
        parent_content,
        f"author {info['author'][0]} <{info['author'][1]}> {commit_time} -0400\n",
        f"committer {info['commiter'][0]} <{info['commiter'][1]}> {commit_time} -0400\n",
        f"\n{message}"
    ]
    commit_str = "".join(commit_contents)
    commit_bytes = commit_str.encode("utf-8")
    header = f"commit {len(commit_str)}\x00"
    header_bytes = header.encode("utf-8")
    compressed = zlib.compress(header_bytes + commit_bytes)

    # produce sha-1 digest of commit
    hasher = hashlib.sha1()
    hasher.update(header_bytes)
    hasher.update(commit_bytes)
    digest = hasher.hexdigest()

    # write to file
    obj_dir = os.path.join('.git', 'objects')
    file_path = os.path.join(obj_dir, digest[:2], digest[2:])
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode="wb+") as commit:
        commit.write(compressed)
    return digest
