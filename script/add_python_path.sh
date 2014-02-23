#!/bin/bash

DIR_ROOT=$(readlink -f $(dirname ${0}))"/../"
echo $DIR_ROOT
DIR_SOURCE=$DIR_ROOT"src/"
echo $DIR_SOURCE

echo "PYTHONPATH=\"\$PYTHONPATH:"$DIR_SOURCE"\"" >> $1
echo 'export PYTHONPATH' >> $1

PYTHONPATH=\"\$PYTHONPATH:"$DIR_SOURCE"\"
export PYTHONPATH