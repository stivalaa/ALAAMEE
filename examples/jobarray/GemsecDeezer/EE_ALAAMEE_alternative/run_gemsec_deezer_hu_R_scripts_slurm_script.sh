#!/bin/bash

#SBATCH --job-name="R_Covariance_gemsec_deezer_hu"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-00:10:00
#SBATCH --output=alaamee_covariance_gemsec_deezer_hu-%j.out
#SBATCH --error=alaamee_covariance_gemsec_deezer_hu-%j.err
#SBATCH --mem=8GB

echo -n "started at: "; date
RSCRIPTSDIR=../../../../R
SCRIPTSDIR=../../../../scripts

uname -a

ESTIM_FILE=estimation_hu.txt

command -v module >/dev/null 2>&1 && module load gcc/11.3.0 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load openmpi/4.1.4 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load r/4.2.1

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_deezer_hu_friendship dzA_values_deezer_hu_friendship

time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_deezer_hu_friendship dzA_values_deezer_hu_friendship | tee ${ESTIM_FILE}

${SCRIPTSDIR}/EEEstimation2textableSingleModel.sh -t ${ESTIM_FILE}
${SCRIPTSDIR}/EEEstimation2textableSingleModel.sh ${ESTIM_FILE} > estimated_model_hu.tex

times
echo -n "ended at: "; date
