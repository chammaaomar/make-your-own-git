import argparse
import os
import sys
import zlib


def git_init(base_dir):
    git_dir = os.path.join(base_dir, ".git")
    obj_dir = os.path.join(git_dir, "objects")
    ref_dir = os.path.join(git_dir, "refs")
    head_f = os.path.join(git_dir, "HEAD")
    os.makedirs(base_dir)
    os.mkdir(git_dir)
    os.mkdir(ref_dir)
    os.mkdir(obj_dir)
    with open(head_f, "w+") as f:
        f.write("ref: refs/heads/master\n")
    print(f"Initialized empty git repository in {git_dir}")

def git_cat(base_dir, digest, print_flag):
    obj_dir = os.path.join(base_dir, '.git', 'objects')
    try:
        blob_path = os.path.join(obj_dir, digest[:2], digest[2:])
    except IndexError:
        print(f"invalid sha-256 digest: {digest}", file=sys.stderr)
        return
    try:
        with open(blob_path, mode="rb") as blob:
            data = blob.read()
            contents = zlib.decompress(data)
            print(str(contents, encoding="utf-8"))
    except FileNotFoundError:
        print(f"digest doesn't correspond to any git object: {digest}", file=sys.stderr)
        return



def main():

    parser = argparse.ArgumentParser(prog="your_git.sh", description="Python clone of the git distributed version control system")
    sub_parsers = parser.add_subparsers(dest="command")

    parser_init = sub_parsers.add_parser("init", help="initialize an empty git repository")
    parser_init.add_argument("-d", "--dir", default=".", help="dir in which to initialize git. Default: .")


    parser_cat = sub_parsers.add_parser("cat-file", help="print zlib-compressed file")
    parser_cat.add_argument("-d", "--dir", default=".", help="dir to search for .git/")
    print_group = parser_cat.add_mutually_exclusive_group(required=True)
    print_group.add_argument("-p", action="store_true", help="pretty-print object's content")
    print_group.add_argument("-t", action="store_true", help="print the object's type")
    print_group.add_argument("-s", action="store_true", help="print the object's size")
    parser_cat.add_argument("object", type=str, help="sha-256 digest of object")

    args = parser.parse_args()

    if args.command == "init":
        git_init(args.dir)
    elif args.command == "cat-file":
        git_cat(args.dir, args.object, args.p)


if __name__ == "__main__":
    main()
