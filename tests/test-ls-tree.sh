#!/usr/bin/env bash

echo "testing git ls-tree"

echo "$(mkdir dir1 dir2)"
echo "$(touch file1 dir1/file_in_dir_{1,2} dir2/file_in_dir_3)"

echo "$(git add file1 dir1/ dir2/)"
TREE_HASH="$(git update-index && git write-tree)"

LS_TREE="$(./your_git.sh ls-tree --name-only $TREE_HASH)"
CORRECT_TREE="$(git ls-tree --name-only $TREE_HASH)"

# clean up
echo "$(rm -rf dir1 dir2)"

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


