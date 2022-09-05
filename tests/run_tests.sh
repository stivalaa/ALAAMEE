#!/bin/sh

module load python/3.9.0

export PYTHONPATH=../python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./tests.py


