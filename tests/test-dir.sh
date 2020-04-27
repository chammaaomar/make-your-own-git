#!/usr/bin/env bash

BASEDIR="$(pwd)"
GITDIR="$BASEDIR/.git"
OBJDIR="$GITDIR/objects"
REFDIR="$GITDIR/refs"
HEADF="$GITDIR/HEAD"

for DIR in $GITDIR $OBJDIR $REFDIR
do
    if [ ! -d "$DIR" ];
    then
        echo "$DIR doesn't exist"
        exit 1
    fi
done

if [ ! -f "$HEADF" ];
then
    echo "$HEADF doesn't exist"
    exit 1
fi

EXPECTED_CAT="ref: refs/heads/master\n"
CAT="$(cat $HEADF)"
if [ "$CAT" != "$EXPECTED_CAT" ];
then
    echo "epected $EXPECTED_CAT \ngot $CAT"
    exit 1
fi
