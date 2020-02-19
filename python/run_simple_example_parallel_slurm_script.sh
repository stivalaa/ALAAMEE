#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=0-01:00:00


# Remember must 'module load R/3.2.5' to get Microsoft R Open 3.2.5 
# otherwise nothing in R works! 
module load R/3.2.5
#module load parallel


uname -a
echo SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK
echo -n "started at: "; date

CPUS_MINUS_ONE=`expr ${SLURM_CPUS_PER_TASK} - 1`

seq 0 ${CPUS_MINUS_ONE} | parallel -j ${SLURM_CPUS_PER_TASK} --progress --joblog parallel.log ./runALAAMEESimpleDemoParallel.py

times
echo -n "ended at: "; date
