![CLI-functional-testing](https://github.com/chammaaomar/make-your-own-git/workflows/CLI-functional-testing/badge.svg)
# Python Git Clone

## codecrafters

Check out the awesome [codecrafters](https://codecrafters.io).

## Usage
This solely uses the Python standard library, so there are no dependancies but Python 3.x. To try it out:
```
git clone https://github.com/chammaaomar/make-your-own-git.git
cd make-your-own-git
./your_git.sh -h
```

will display the commands that have been implemented thus far with (hopefully) helpful usage messages. The main commands are

- `init`
- `cat-file`: Works with trees and blobs. Currently requires the full 40-char SHA-1.
- `hash-object`
- `ls-tree`: Currently only works with the `--name-only` option, and requires the full 40-char SHA-1.
- `write-tree`
- `commit-tree`

You can use `./your_git cmd -h`, where `cmd` is one of the above, for command-specific help, e.g.

```
>>> ./your_git cat-file -h
>>> usage: your_git.sh cat-file [-h] (-p | -t | -s) object

positional arguments:
  object      sha-1 digest of object

optional arguments:
  -h, --help  show this help message and exit
  -p          pretty-print object's content
  -t          print the object's type
  -s          print the object's size
```
