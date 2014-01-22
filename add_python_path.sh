#!/bin/bash

DIR_ROOT=$(readlink -f $(dirname ${0}))"/"
DIR_SOURCE=$DIR_ROOT"src/"

echo "PYTHONPATH=\"\$PYTHONPATH:"$DIR_SOURCE"\"" >> $1
echo 'export PYTHONPATH' >> $1
