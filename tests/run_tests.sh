#!/bin/sh

echo -n "started at: "; date
uname -a
command -v module >/dev/null 2>&1 && module load python/3.9.0

export PYTHONPATH=../python:${PYTHONPATH}
#export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./tests.py
echo -n "ended at: "; date


