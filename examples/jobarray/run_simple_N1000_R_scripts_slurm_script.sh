#!/bin/bash

#SBATCH --job-name="R_Covariance_simple_example"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_covariance_simexampleN1000-%j.out
#SBATCH --error=alaamee_covariance_simexampleN1000-%j.err

echo -n "started at: "; date

module unload python # must do this otherwise module load r fails on cluster
module load r 


uname -a

ESTIM_FILE=estimation_simple_N1000.txt

time Rscript ../../R/plotALAAMEEResults.R theta_values_n1000_kstar_simulate12750000 dzA_values_n1000_kstar_simulate12750000


time Rscript ../../R/computeALAMEEcovariance.R theta_values_n1000_kstar_simulate12750000 dzA_values_n1000_kstar_simulate12750000 | tee ${ESTIM_FILE}

../../scripts/EEEstimation2textableSingleModel.sh -t ${ESTIM_FILE}

times
echo -n "ended at: "; date
