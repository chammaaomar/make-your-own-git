#!/usr/bin/env bash

echo "testing git ls-tree"

echo "$(mkdir dir1 dir2)"
echo "$(touch file1 dir1/file_in_dir_{1,2} dir2/file_in_dir_3)"

echo "$(git add file1 dir1/ dir2/)"
echo "$(git commit -m \"test\")"
TREE_HASH="192403f9d8c4872a30e949685d9e5e7f91f06933"

LS_TREE="$(./your_git.sh ls-tree --name-only $TREE_HASH)"
CORRECT_TREE="$(git ls-tree --name-only $TREE_HASH)"
if [[ "$LS_TREE" == "$CORRECT_TREE" ]];
then
    echo "git ls-tree passing"
    exit 0
else
    echo "Expected the following tree structure:"
    echo "$CORRECT_TREE"
    echo "instead got:"
    echo "$LS_TREE"
    exit 1
fi


