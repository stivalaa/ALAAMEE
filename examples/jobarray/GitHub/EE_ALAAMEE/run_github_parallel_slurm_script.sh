#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel"
#SBATCH --time=0-04:00:00
#SBATCH --output=alaamee_Github-%j.out
#SBATCH --error=alaamee_Github-%j.err
#SBATCH --ntasks=10
#SBATCH --mem-per-cpu=100MB
#SBATCH --partition=slim


echo -n "started at: "; date

ROOT=../../../..

#NUM_RUNS=10
NUM_RUNS=2

echo NUM_RUNS = $NUM_RUNS
NUM_RUNS_MINUS_ONE=`expr ${NUM_RUNS} - 1`

module load python/3.9.0

export PYTHONPATH=${ROOT}/python/:${PYTHONPATH}
python3 ./runALAAMEEGithubParallel.py ${SLURM_ARRAY_TASK_ID}

# use default (no --jobs option) jobs in parallel (one per CPU default)
#seq 0 ${NUM_RUNS_MINUS_ONE} | parallel --progress --joblog parallel.log ./runALAAMEEGithubParallel.py

seq 0 ${NUM_RUNS_MINUS_ONE} | parallel --jobs 6 --progress --joblog parallel.log ./runALAAMEEGithubParallel.py



times
echo -n "ended at: "; date
