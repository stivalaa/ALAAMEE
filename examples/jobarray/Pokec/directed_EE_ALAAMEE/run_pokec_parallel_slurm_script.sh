#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel"
#SBATCH --time=0-4:00:00
#SBATCH --output=alaamee_pokec-%j.out
#SBATCH --error=alaamee_pokec-%j.err
#SBATCH --ntasks=20
#SBATCH --mem-per-cpu=6GB

uname -a
echo -n "started at: "; date

#module load python/3.9.0

#NUM_RUNS=20
NUM_RUNS=2

echo NUM_RUNS = $NUM_RUNS
NUM_RUNS_MINUS_ONE=`expr ${NUM_RUNS} - 1`

ROOT=${DOCUMENTS}/USI/ALAAMEE
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs
export PYTHONPATH=${ROOT}/python/:${PYTHONPATH}

# use default (no --jobs option) jobs in parallel (one per CPU default)
#seq 0 ${NUM_RUNS_MINUS_ONE} | parallel --progress --joblog parallel.log ./runALAAMEEpokecParallel.py

seq 0 ${NUM_RUNS_MINUS_ONE} | parallel --jobs 6 --progress --joblog parallel.log ./runALAAMEEpokecParallel.py


times
echo -n "ended at: "; date
