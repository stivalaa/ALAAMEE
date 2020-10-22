#!/bin/bash

#SBATCH --job-name="R_Covariance_simple_example"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_covariance_simexample-%j.out
#SBATCH --error=alaamee_covariance_simexample-%j.err


#module load R/3.2.5
module load r  #r/4.0.2-gcc-10.1.0-4w3buai

uname -a

time Rscript ../..//R/plotALAAMEEResults.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000


time Rscript ../..//R/computeALAMEEcovariance.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000

times
echo -n "ended at: "; date
