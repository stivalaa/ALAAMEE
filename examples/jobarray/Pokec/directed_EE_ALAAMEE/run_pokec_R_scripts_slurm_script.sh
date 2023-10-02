#!/bin/bash

#SBATCH --job-name="R_Covariance_pokec"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-00:20:00
#SBATCH --output=alaamee_covariance_pokec-%j.out
#SBATCH --error=alaamee_covariance_pokec-%j.err
#SBATCH --mem=8GB

echo -n "started at: "; date

module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

RSCRIPTSDIR=${HOME}/ALAAMEE/R
#RSCRIPTSDIR=${DOCUMENTS}/USI/ALAAMEE/R

uname -a

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_soc-pokec-relationships-directed dzA_values_soc-pokec-relationships-directed


time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_soc-pokec-relationships-directed dzA_values_soc-pokec-relationships-directed | tee estimation.txt

times
echo -n "ended at: "; date
