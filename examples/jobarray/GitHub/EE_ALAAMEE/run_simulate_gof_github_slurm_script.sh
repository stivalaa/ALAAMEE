#!/bin/sh
#SBATCH --job-name="gof_ALAAM"
#SBATCH --time=0-04:00:00
#SBATCH --output=gof_alaam_sim_github-%j.out
#SBATCH --error=gof_alaam_sim_github-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=4GB
#SBATCH --partition=slim

echo -n "started at: "; date
uname -a

module purge    # otherwise module load python sometimes fails
module load python/3.9.0

# run simulation from parameters and plot observed
# statistics of network from which the parmeters were estimated as
# GoF check

# output file of simulated ALAAM statistics
SIMSTATS_FILE=stats_sim_gof_musae_git.txt

# output file of observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_musae_git.txt

ROOT=../../../../
export PYTHONPATH=${ROOT}/python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./computeALAAMstatisticsGithub.py | tee ${OBSTATS_FILE}

# TODO parse parameters for simulation from estimation output (currently 
#      hardcoded in ./runALAAMsimulateGoFGithub.py  script)
time python3 ./runALAAMsimulateGoFGithub.py  | tee ${SIMSTATS_FILE}


module unload python # otherwise module load r fails
module load r
Rscript ${ROOT}/R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}


times
echo -n "started at: "; date
