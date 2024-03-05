#!/bin/bash

#SBATCH --job-name="R_Covariance_gemsec_deezer_hr"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-00:10:00
#SBATCH --output=alaamee_covariance_gemsec_deezer_hr-%j.out
#SBATCH --error=alaamee_covariance_gemsec_deezer_hr-%j.err
#SBATCH --mem=8GB

echo -n "started at: "; date
RSCRIPTSDIR=../../../../R

uname -a

command -v module >/dev/null 2>&1 && module load gcc/11.3.0 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load openmpi/4.1.4 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load r/4.2.1

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_deezer_hr_friendship dzA_values_deezer_hr_friendship

time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_deezer_hr_friendship dzA_values_deezer_hr_friendship | tee estimation_hr.txt

times
echo -n "ended at: "; date
