#!/bin/bash

#SBATCH --job-name="R_Covariance_simple_example"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_covariance_simexample-%j.out
#SBATCH --error=alaamee_covariance_simexample-%j.err


# Remember must 'module load R/3.2.5' to get Microsoft R Open 3.2.5 
# otherwise nothing in R works! 
module load R/3.2.5


uname -a

time Rscript ../..//R/plotALAAMEEResults.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000


time Rscript ../..//R/computeALAMEEcovariance.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000

times
echo -n "ended at: "; date
