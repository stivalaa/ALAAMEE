#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel_sim"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_simexample-%j.out
#SBATCH --error=alaamee_simexample-%j.err



uname -a
echo SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK
echo -n "started at: "; date

NUM_RUNS=100

echo NUM_RUNS = $NUM_RUNS
NUM_RUNS_MINUS_ONE=`expr ${NUM_RUNS} - 1`

# use default (no --jobs option) jobs in parallel (one per CPU default)
seq 0 ${NUM_RUNS_MINUS_ONE} | parallel --progress --joblog parallel.log ../../python/runALAAMEESimpleDemoParallel.py


module load r

Rscript ../../R/plotALAAMEEResults.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000


Rscript ../../R/computeALAMEEcovariance.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000

times
echo -n "ended at: "; date
