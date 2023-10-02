#!/bin/bash

#SBATCH --job-name="R_Covariance_Deezer"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-00:10:00
#SBATCH --output=alaamee_covariance_Deezer-%j.out
#SBATCH --error=alaamee_covariance_Deezer-%j.err
#SBATCH --partition=slim

echo -n "started at: "; date

module load r

RSCRIPTSDIR=${HOME}/ALAAMEE/R

uname -a

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_deezer_europe dzA_values_deezer_europe


time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_deezer_europe dzA_values_deezer_europe | tee estimation.txt

times
echo -n "ended at: "; date
