#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel_karate"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=0-10:00:00
#SBATCH --output=alaamee_karate-%j.out
#SBATCH --error=alaamee_karate-%j.err


uname -a
echo SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK
echo -n "started at: "; date

NUM_RUNS=100
NUM_RUNS_MINUS_ONE=`expr ${NUM_RUNS} - 1`

# use default (no --jobs option) jobs in parallel (one per CPU default)
seq 0 ${NUM_RUNS_MINUS_ONE} | parallel  --progress --joblog parallel.log ../../python/runALAAMEEkarateClubParallel.py


module load r

Rscript ../../R/plotALAAMEEResults.R theta_values_karate dzA_values_karate


Rscript ../../R/computeALAMEEcovariance.R theta_values_karate dzA_values_karate

times
echo -n "ended at: "; date
