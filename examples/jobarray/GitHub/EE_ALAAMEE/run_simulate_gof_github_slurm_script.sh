#!/bin/sh
#SBATCH --job-name="gof_ALAAM"
#SBATCH --time=0-01:00:00
#SBATCH --output=gof_alaam_sim_github-%j.out
#SBATCH --error=gof_alaam_sim_github-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=4GB

echo -n "started at: "; date
uname -a

#module purge    # otherwise module load python sometimes fails
#module load python/3.9.0
# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02

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

time python3 ./runALAAMsimulateGoFGithub.py  | tee ${SIMSTATS_FILE}

module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

Rscript ${ROOT}/R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}

./plot_model_degeneracy_check.sh

Rscript ${ROOT}/R/plotALAAMEEsimFit.R ../data/musae_git.net ../data/musae_git_target.txt  sim_outcome

times
echo -n "started at: "; date
