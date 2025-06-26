#!/bin/bash

#SBATCH --job-name="R_Covariance_pokec"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_covariance_pokec-%j.out
#SBATCH --error=alaamee_covariance_pokec-%j.err

echo -n "started at: "; date

module load r

#RSCRIPTSDIR=${HOME}/ALAAMEE/R
ROOT=../../../../
RSCRIPTSDIR=${ROOT}/R
SCRIPTSDIR=${ROOT}/scripts

uname -a

ESTIM_FILE=estimation.txt

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_soc-pokec-relationships-undirected dzA_values_soc-pokec-relationships-undirected


time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_soc-pokec-relationships-undirected dzA_values_soc-pokec-relationships-undirected | tee estimation.txt

${SCRIPTSDIR}/EEEstimation2textableSingleModel.sh -t ${ESTIM_FILE}
${SCRIPTSDIR}/EEEstimation2textableSingleModel.sh ${ESTIM_FILE} > estimated_model.tex

times
echo -n "ended at: "; date
