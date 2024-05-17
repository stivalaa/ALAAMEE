#!/bin/sh
#SBATCH --job-name="gof_ALAAM"
#SBATCH --time=0-04:00:00
#SBATCH --output=gof_alaam_sim_StLouisCrime-%j.out
#SBATCH --error=gof_alaam_sim_StLouisCrime-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=1GB

command -v module >/dev/null 2>&1 && module purge    # otherwise module load python sometimes fails
command -v module >/dev/null 2>&1 && module load python/3.9.0

# run simulation from parameters and plot observed
# statistics of network from which the parmeters were estimated as
# GoF check

# output file of simulated ALAAM statistics
SIMSTATS_FILE=stats_sim_gof_evtusehnko_bipartite.txt

# output file of observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_evtusehnko_bipartite.txt

#export PYTHONPATH=${HOME}/ALAAMEE/python:${PYTHONPATH}
export PYTHONPATH=${DOCUMENTS}/USI/ALAAMEE/python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time ./computeALAAMstatisticsStLouisCrime.py | tee ${OBSTATS_FILE}
time ./runALAAMsimulateGoFStLouisCrime.py  | tee ${SIMSTATS_FILE}


command -v module >/dev/null 2>&1 && module unload python # otherwise module load r fails
command -v module >/dev/null 2>&1 && module load r

#Rscript ${HOME}/ALAAMEE/R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}
Rscript ${DOCUMENTS}/USI/ALAAMEE/R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}


