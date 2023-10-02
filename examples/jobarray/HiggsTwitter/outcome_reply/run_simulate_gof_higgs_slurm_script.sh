#!/bin/sh
#SBATCH --job-name="gof_ALAAM"
#SBATCH --time=0-04:00:00
#SBATCH --output=gof_alaam_sim_higgs-%j.out
#SBATCH --error=gof_alaam_sim_higgs-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=4GB

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
SIMSTATS_FILE=stats_sim_gof_higgs.txt

# output file of observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_higgs.txt

ROOT=${HOME}
export PYTHONPATH=${ROOT}/ALAAMEE/python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

#if [ ! -f ${OBSTATS_FILE} ]; then
  time ./computeALAAMstatisticsHiggs.py | tee ${OBSTATS_FILE}
#fi

time ./runALAAMsimulateGoFHiggs.py  | tee ${SIMSTATS_FILE}


module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

Rscript ${ROOT}/ALAAMEE/R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}


times
echo -n "ended at: "; date
