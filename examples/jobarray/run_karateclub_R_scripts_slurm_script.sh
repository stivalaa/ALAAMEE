#!/bin/bash

#SBATCH --job-name="R_Covariance_karateclub"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_covariance_karate-%j.out
#SBATCH --error=alaamee_covariance_karate-%j.err

echo -n "started at: "; date

module unload python # must do this otherwise module load r fails on cluster
module load r 


uname -a

time Rscript ../../R/plotALAAMEEResults.R theta_values_karate dzA_values_karate


time Rscript ../../R/computeALAMEEcovariance.R theta_values_karate dzA_values_karate

times
echo -n "ended at: "; date
