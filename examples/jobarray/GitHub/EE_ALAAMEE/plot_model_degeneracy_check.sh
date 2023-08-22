#!/bin/sh
#
# Extract stats in model only from simulation output and plot diagnostics
#

module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02

# simulated ALAAM statistics
SIMSTATS_FILE=stats_sim_gof_musae_git.txt

# observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_musae_git.txt

# output: simulated ALAAM statistics, but only those in the model
MODEL_SIMSTATS_FILE=model_stats_sim_gof_musae_git.txt

ROOT=../../../../
export PYTHONPATH=${ROOT}/python:${PYTHONPATH}

python3 ./extractModelStats.py ${SIMSTATS_FILE} > ${MODEL_SIMSTATS_FILE}

module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

Rscript ${ROOT}/R/plotSimulationDiagnostics.R  ${MODEL_SIMSTATS_FILE} ${OBSTATS_FILE}


