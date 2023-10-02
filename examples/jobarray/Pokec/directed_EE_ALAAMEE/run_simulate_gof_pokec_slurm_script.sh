#!/bin/sh
#SBATCH --job-name="gof_ALAAM"
#SBATCH --time=0-10:00:00
#SBATCH --output=gof_alaam_sim_pokec-%j.out
#SBATCH --error=gof_alaam_sim_pokec-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=8GB

echo -n "started at: "; date
uname -a

# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02


# run simulation from parameters and plot observed
# statistics of network from which the parmeters were estimated as
# GoF check

# output file of simulated ALAAM statistics
SIMSTATS_FILE=stats_sim_gof_pokec.txt

# output file of observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_pokec.txt

#ROOT=${DOCUMENTS}/USI
ROOT=${HOME}
export PYTHONPATH=${ROOT}/ALAAMEE/python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time ./computeALAAMstatisticsPokec.py | tee ${OBSTATS_FILE}

time ./runALAAMsimulateGoFPokec.py  | tee ${SIMSTATS_FILE}


module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

Rscript ${ROOT}/ALAAMEE/R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}


times
echo -n "ended at: "; date
