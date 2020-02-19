#!/bin/bash

#SBATCH --job-name="ALAAMEE_jobarray_parallel_sim"
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_simexample-%A_%a.out
#SBATCH --error=alaamee_simexample-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --array=1-4


# Remember must 'module load R/3.2.5' to get Microsoft R Open 3.2.5 
# otherwise nothing in R works! 
#module load R/3.2.5

uname -a
echo -n "started at: "; date

echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

python ./runALAAMEESimpleDemoParallel.py ${SLURM_ARRAY_TASK_ID}

#Rscript ../R/plotALAAMEEResults.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000


#Rscript ../R/computeALAMEEcovariance.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000

times
echo -n "ended at: "; date
