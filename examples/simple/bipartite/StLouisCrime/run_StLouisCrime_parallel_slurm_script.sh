#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel"
#SBATCH --time=0-02:00:00
#SBATCH --output=alaamee_StLouisCrime-%j.out
#SBATCH --error=alaamee_StLouisCrime-%j.err
#SBATCH --ntasks=10
#SBATCH --mem-per-cpu=200MB


echo -n "started at: "; date
uname -a

#NUM_RUNS=10
NUM_RUNS=6

echo NUM_RUNS = $NUM_RUNS
NUM_RUNS_MINUS_ONE=`expr ${NUM_RUNS} - 1`

command -v module >/dev/null 2>&1 && module load python/3.9.0

#export PYTHONPATH=${HOME}/ALAAMEE/python/:${PYTHONPATH}
export PYTHONPATH=../../../../python/:${PYTHONPATH}

# use default (no --jobs option) jobs in parallel (one per CPU default)
#seq 0 ${NUM_RUNS_MINUS_ONE} | parallel --progress --joblog parallel.log python3 ./runALAAMEEStLouisCrimeParallel.py

seq 0 ${NUM_RUNS_MINUS_ONE} | parallel --jobs 6 --progress --joblog parallel.log python3 ./runALAAMEEStLouisCrimeParallel.py

times
echo -n "ended at: "; date
