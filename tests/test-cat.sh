#!/usr/bin/env bash
echo "testing git cat-file"

phrase="This is a test"
digest="$(echo $phrase | git hash-object --stdin -w)"
decompressed="$(./your_git.sh cat-file -p $digest)"

if [[ "$decompressed" == "$phrase" ]];
then
    echo "git cat-file test passing!"
    echo "cleaning up..."
    echo "$(rm -rf .git/objects/05/27e6bd2d76b45e2933183f1b506c7ac49f5872)"
    exit 0
else
    echo "expected \"$phrase\", instead got: \"$decompressed\""
    exit 1
fi