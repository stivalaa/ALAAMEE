#!/bin/sh

echo -n "started at: "; date
uname -a
command -v module >/dev/null 2>&1 && module load python/3.9.0

export PYTHONPATH=../python:${PYTHONPATH}
#export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

fail=0
time python3 ./tests.py || fail=1
time python3 ./tests_igraph.py || fail=1

if [ $fail -ne 0 ]; then
    echo "***** A test FAILED *****"
fi
echo -n "ended at: "; date
exit $fail


