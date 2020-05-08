#!/usr/bin/env bash
echo "testing git hash-object"

phrase="Am I doing TDD yet?"
digest="$(echo $phrase > test && ./your_git.sh hash-object -w test)"
hash="8506ab8b90134d918d6c9fa75e1071ef7a47a094"

if [[ "$hash" != "$digest" ]];
then
    echo "Expected sha-1 id of \"$phrase\" to be $hash"
    echo "instead got $digest"
    exit 1
fi

decompressed="$(git cat-file -p $digest)"

if [[ "$decompressed" != "$phrase" ]];
then
    echo "Expected to get original phrase: \"$phrase\""
    echo "instead got \"$decompressed\""
    exit 1
fi

echo "cleaning up..."
echo "$(rm -rf .git/objects/85/06ab8b90134d918d6c9fa75e1071ef7a47a094)"

echo "git hash-object test passing!"