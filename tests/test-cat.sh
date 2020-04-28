#!/usr/bin/env bash
phrase="This is a test"
digest="$(echo $phrase | git hash-object --stdin -w)"
decompressed="$(./your_git.sh cat-file -p $digest)"

if [[ "$decompressed" == "$phrase" ]];
then
    echo "git cat-file test passing!"
    exit 0
else
    echo "expected \"$phrase\", instead got: \"$decompressed\""
    exit 1
fi
