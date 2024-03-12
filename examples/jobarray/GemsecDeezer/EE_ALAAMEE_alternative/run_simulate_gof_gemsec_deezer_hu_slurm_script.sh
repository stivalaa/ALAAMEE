#!/bin/sh
#SBATCH --job-name="gof_ALAAM_GEMSEC_HU"
#SBATCH --time=0-02:00:00
#SBATCH --output=gof_alaam_sim_gemsec_deezer_hu-%j.out
#SBATCH --error=gof_alaam_sim_gemsec_deezer_hu-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=4GB

echo -n "started at: "; date
uname -a

# module version numbers are required on OzStar (Ngarrgu Tindebeek)
command -v module >/dev/null 2>&1 && module load foss/2022b
command -v module >/dev/null 2>&1 && module load python/3.10.8
command -v module >/dev/null 2>&1 && module load numpy/1.24.2-scipy-bundle-2023.02

# run simulation from parameters and plot observed
# statistics of network from which the parmeters were estimated as
# GoF check

# output file of simulated ALAAM statistics
SIMSTATS_FILE=stats_sim_gof_deezer_hu.txt

# output file of observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_deezer_hu.txt

ROOT=../../../../

export PYTHONPATH=${ROOT}/python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./computeALAAMstatisticsGemsecDeezerHU.py | tee ${OBSTATS_FILE}

time python3 ./runALAAMsimulateGoFGemsecDeezerHU.py  | tee ${SIMSTATS_FILE}

command -v module >/dev/null 2>&1 && module load gcc/11.3.0 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load openmpi/4.1.4 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load r/4.2.1

Rscript ${ROOT}/R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}

Rscript ${ROOT}/R/plotALAAMEEsimFit.R -a -e ../data/deezer_hu_friendship.net ../data/deezer_hu_outcome_alternative.txt sim_deezer_hu_outcome_alternative

times
echo -n "ended at: "; date
