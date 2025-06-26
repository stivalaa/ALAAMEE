#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel_karate"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=0-4:00:00
#SBATCH --output=alaamee_karate-%j.out
#SBATCH --error=alaamee_karate-%j.err


uname -a
echo SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK
echo -n "started at: "; date

module load python/3.9.0

NUM_RUNS=40
NUM_RUNS_MINUS_ONE=`expr ${NUM_RUNS} - 1`

ESTIM_FILE=estimation_karateclub.txt

# use default (no --jobs option) jobs in parallel (one per CPU default)
seq 0 ${NUM_RUNS_MINUS_ONE} | parallel  --progress --joblog parallel.log ../../python/runALAAMEEkarateClubParallel.py


module unload python # on cluster module load r will not work if this is not done
module load r


Rscript ../../R/plotALAAMEEResults.R theta_values_karate dzA_values_karate


Rscript ../../R/computeALAMEEcovariance.R theta_values_karate dzA_values_karate | tee ${ESTIM_FILE}

../../scripts/EEEstimation2textableSingleModel.sh -t ${ESTIM_FILE}

times
echo -n "ended at: "; date
