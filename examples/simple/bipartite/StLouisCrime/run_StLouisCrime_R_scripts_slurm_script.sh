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
RSCRIPTSDIR=../../../../R

uname -a

time Rscript ${RSCRIPTSDIR}/plotALAAMEEResults.R theta_values_crime_bipartite dzA_values_crime_bipartite


time Rscript ${RSCRIPTSDIR}/computeALAMEEcovariance.R theta_values_crime_bipartite dzA_values_crime_bipartite | tee estimation_StLouisCrime_bipartite.txt

times
echo -n "ended at: "; date

