#!/usr/bin/env bash

echo "testing git write-tree"

echo "$(mkdir -p dir/another)"
echo "$(touch dir/file{1,2} dir/another/file3)"

TREE_HASH="$(./your_git.sh write-tree)"
CORRECT_HASH="$(git add . && git write-tree)"

# clean up
echo "$(rm -rf dir)"

if [[  "$TREE_HASH" == "$CORRECT_HASH" ]];
then
    echo "git write-tree passing"
    exit 0
else
    echo "Expected the following tree hash:"
    echo "$CORRECT_HASH"
    echo "instead got:"
    echo "$TREE_HASH"
    exit 1
fi