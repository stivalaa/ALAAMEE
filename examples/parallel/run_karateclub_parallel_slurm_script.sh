#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel_karate"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_karate-%j.out
#SBATCH --error=alaamee_karate-%j.err


# Remember must 'module load R/3.2.5' to get Microsoft R Open 3.2.5 
# otherwise nothing in R works! 
module load R/3.2.5
#module load parallel


uname -a
echo SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK
echo -n "started at: "; date

CPUS_MINUS_ONE=`expr ${SLURM_CPUS_PER_TASK} - 1`

seq 0 ${CPUS_MINUS_ONE} | parallel -j ${SLURM_CPUS_PER_TASK} --progress --joblog parallel.log ../../python/runALAAMEEkarateClubParallel.py

Rscript ../../R/plotALAAMEEResults.R theta_values_karate dzA_values_karate


Rscript ../../R/computeALAMEEcovariance.R theta_values_karate dzA_values_karate

times
echo -n "ended at: "; date
