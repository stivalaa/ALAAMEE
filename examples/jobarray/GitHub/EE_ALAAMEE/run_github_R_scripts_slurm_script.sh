#!/bin/bash

#SBATCH --job-name="R_Covariance_Github"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-00:10:00
#SBATCH --output=alaamee_covariance_Github-%j.out
#SBATCH --error=alaamee_covariance_Github-%j.err
#SBATCH --partition=slim
#SBATCH --mem=8GB


module load r

RSCRIPTSDIR=${HOME}/ALAAMEE/R

uname -a

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_musae_git dzA_values_musae_git


time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_musae_git dzA_values_musae_git | tee estimation.txt

times
echo -n "ended at: "; date
