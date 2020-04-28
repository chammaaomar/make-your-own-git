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
        help="print zlib-compressed file")
    parser_hash = sub_parsers.add_parser(
        "hash-object",
        help=(
            "writes to stdout the content-addressable id (sha-1 digest) "
            "that would be used to store object in object database"
            )
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
        help="actually writes the object into .git/objects"
    )
    parser_hash.add_argument(
        "file",
        help="/full/path/to/file"
    )

    args = parser.parse_args()

    if args.command == "init":
        plumbing.init(args.dir)
    elif args.command == "cat-file":
        plumbing.cat_file(args.object, args.print_flag)
    elif args.command == "hash-object":
        plumbing.hash_object(args.file, args.write)

if __name__ == "__main__":
    main()