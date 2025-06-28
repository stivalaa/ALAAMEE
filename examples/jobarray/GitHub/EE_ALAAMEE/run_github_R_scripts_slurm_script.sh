#!/bin/bash

#SBATCH --job-name="R_Covariance_Github"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-00:10:00
#SBATCH --output=alaamee_covariance_Github-%j.out
#SBATCH --error=alaamee_covariance_Github-%j.err
#SBATCH --mem=8GB

echo -n "started at: "; date

#RSCRIPTSDIR=${HOME}/ALAAMEE/R
RSCRIPTSDIR=../../../../R
SCRIPTSDIR=../../../../scripts

uname -a

ESTIM_FILE=estimation.txt

module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_musae_git dzA_values_musae_git


time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_musae_git dzA_values_musae_git | tee ${ESTIM_FILE}

${SCRIPTSDIR}/EEEstimation2textableSingleModel.sh -t ${ESTIM_FILE}
${SCRIPTSDIR}/EEEstimation2textableSingleModel.sh ${ESTIM_FILE} > estimated_model.tex

times
echo -n "ended at: "; date
