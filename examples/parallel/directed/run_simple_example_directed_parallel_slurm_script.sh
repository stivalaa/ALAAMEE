#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel_directed"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=0-02:00:00
#SBATCH --output=alaamee_directede_example-%j.out
#SBATCH --error=alaamee_directed_example-%j.err



uname -a
echo SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK
echo -n "started at: "; date

module load python/3.8.5

NUM_RUNS=40

echo NUM_RUNS = $NUM_RUNS
NUM_RUNS_MINUS_ONE=`expr ${NUM_RUNS} - 1`

# use default (no --jobs option) jobs in parallel (one per CPU default)
seq 0 ${NUM_RUNS_MINUS_ONE} | parallel --progress --joblog parallel.log ../../../python/runALAAMEESimpleDemoParallelDirected.py


module unload python # on cluster module load r will not work if this is not done
module load r

Rscript ../../../R/plotALAAMEEResults.R theta_values_highschool_friendship_arclist dzA_values_highschool_friendship_arclist


Rscript ../../../R/computeALAMEEcovariance.R theta_values_highschool_friendship_arclist dzA_values_highschool_friendship_arclist

times
echo -n "ended at: "; date
