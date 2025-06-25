#!/bin/bash

#SBATCH --job-name="R_Covariance_StLouisCrime"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-01:00:00
#SBATCH --mem=2GB
#SBATCH --output=alaamee_covariance_StLouisCrime-%j.out
#SBATCH --error=alaamee_covariance_StLouisCrime-%j.err

echo -n "started at: "; date

command -v module >/dev/null 2>&1 && module load r

#RSCRIPTSDIR=${HOME}/ALAAMEE/R
ROOT=../../../../
RSCRIPTSDIR=${ROOT}/R
SCRIPTSDIR=${ROOT}/scripts

uname -a

ESTIM_FILE=estimation_StLouisCrime_bipartite.txt

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_crime_bipartite dzA_values_crime_bipartite


time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_crime_bipartite dzA_values_crime_bipartite | tee ${ESTIM_FILE}

${SCRIPTSDIR}/EEEstimation2textableSingleModel.sh -t ${ESTIM_FILE}
${SCRIPTSDIR}/EEEstimation2textableSingleModel.sh  ${ESTIM_FILE} > estimated_model_StLouisCrime_bipartite.tex

times
echo -n "ended at: "; date

