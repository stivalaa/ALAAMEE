#!/bin/bash

#SBATCH --job-name="R_Covariance_higgs"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-00:10:00
#SBATCH --output=alaamee_covariance_higgs-%j.out
#SBATCH --error=alaamee_covariance_higgs-%j.err
#SBATCH --mem-per-cpu=8GB

echo -n "started at: "; date

#module load r
module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

RSCRIPTSDIR=${HOME}/ALAAMEE/R

uname -a

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_higgs_social dzA_values_higgs_social


time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_higgs_social dzA_values_higgs_social | tee estimation.txt

times
echo -n "ended at: "; date
