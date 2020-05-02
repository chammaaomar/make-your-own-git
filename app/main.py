import argparse

import app.plumbing as plumbing 
from app.consts import *


def main():

    parser = argparse.ArgumentParser(
        prog="your_git.sh",
        description="Python clone of the git distributed version control system")
    sub_parsers = parser.add_subparsers(dest="command")

    # main commands
    parser_init = sub_parsers.add_parser(
        "init",
        help="initialize an empty git repository")
    parser_cat = sub_parsers.add_parser(
        "cat-file",
        help="print the contents of a blob object")
    parser_hash = sub_parsers.add_parser(
        "hash-object",
        help=(
            "write to stdout the content-addressing id (sha-1 digest) "
            "that would be used to store the object in the git object database"
            )
    )
    parser_lstree = sub_parsers.add_parser(
        "ls-tree",
        help="list the contents of a tree object"
    )

    # init command options
    parser_init.add_argument(
        "-d",
        "--dir",
        default=".",
        help="dir in which to initialize git. Default: .")

    # cat-file command options
    print_group = parser_cat.add_mutually_exclusive_group(required=True)
    print_group.add_argument(
        "-p",
        action="store_const",
        const=P_FL,
        dest='print_flag',
        help="pretty-print object's content")
    print_group.add_argument(
        "-t",
        action="store_const",
        const=T_FL,
        dest='print_flag',
        help="print the object's type")
    print_group.add_argument(
        "-s",
        action="store_const",
        const=S_FL,
        dest='print_flag',
        help="print the object's size")
    parser_cat.add_argument(
        "object",
        type=str,
        help="sha-1 digest of object")
    
    # hash-object command options
    parser_hash.add_argument(
        "-w",
        "--write",
        action="store_true",
        help="actually write the object into .git/objects"
    )
    parser_hash.add_argument(
        "file",
        help="/full/path/to/file"
    )

    # tree-ls command options
    lsfmt_group = parser_lstree.add_mutually_exclusive_group()
    lsfmt_group.add_argument(
        "--name-only",
        action="store_const",
        const=NAMEONLY_FL,
        dest="lsfmt_flag",
        help="list only the names of blobs / trees within the tree"
    )
    lsfmt_group.add_argument(
        "--long",
        "-l",
        action="store_const",
        const=LONG_FL,
        dest="lsfmt_flag",
        help="additionally list the size of the object"
    )
    parser_lstree.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="recursively list objects in subtrees"
    )
    parser_lstree.add_argument(
        "tree",
        help="content-addressing id (sha-1 digest) of tree"
    )

    args = parser.parse_args()

    # dispatching calls

    if args.command == "init":
        plumbing.init(args.dir)
    elif args.command == "cat-file":
        plumbing.cat_file(args.object, args.print_flag)
    elif args.command == "hash-object":
        plumbing.hash_object(args.file, args.write)
    elif args.command == "tree-ls":
        plumbing.ls_tree(
            args.tree,
            args.lsfmt_flag,
            args.recursive
        )

if __name__ == "__main__":
    main()