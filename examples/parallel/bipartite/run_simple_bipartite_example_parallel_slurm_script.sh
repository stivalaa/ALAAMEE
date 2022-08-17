#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel_bipartite"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=0-02:00:00
#SBATCH --output=alaamee_bipartite_inouye-%j.out
#SBATCH --error=alaamee_bipartite_inouye-%j.err



uname -a
echo SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK
echo -n "started at: "; date

module load python/3.8.5

NUM_RUNS=40

echo NUM_RUNS = $NUM_RUNS
NUM_RUNS_MINUS_ONE=`expr ${NUM_RUNS} - 1`

# use default (no --jobs option) jobs in parallel (one per CPU default)
seq 0 ${NUM_RUNS_MINUS_ONE} | parallel --progress --joblog parallel.log ../../python/runALAAMEEBipartiteDemoParallel.py


module unload python # on cluster module load r will not work if this is not done
module load r

Rscript ../../R/plotALAAMEEResults.R theta_values_inouye dzA_values_inouye


Rscript ../../R/computeALAMEEcovariance.R theta_values_inouye dzA_values_inouye

times
echo -n "ended at: "; date
