#!/bin/bash

#SBATCH --job-name="ALAAMEE_parallel_sim"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_simexample-%j.out
#SBATCH --error=alaamee_simexample-%j.err


# Remember must 'module load R/3.2.5' to get Microsoft R Open 3.2.5 
# otherwise nothing in R works! 
module load R/3.2.5
#module load parallel


uname -a
echo SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK
echo -n "started at: "; date

CPUS_MINUS_ONE=`expr ${SLURM_CPUS_PER_TASK} - 1`

seq 0 ${CPUS_MINUS_ONE} | parallel -j ${SLURM_CPUS_PER_TASK} --progress --joblog parallel.log ./runALAAMEESimpleDemoParallel.py


Rscript ../R/computeALAMEEcovariance.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000

Rscript ../R/plotALAAMEEresults theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000

times
echo -n "ended at: "; date
