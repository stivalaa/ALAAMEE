#!/bin/sh
#SBATCH --job-name="gof_ALAAM"
#SBATCH --time=0-0:10:00
#SBATCH --output=gof_alaam_sim_example-%j.out
#SBATCH --error=gof_alaam_sim_example-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=2GB

module load python/3.9.0

# example to run simulation from parameters and plot observed
# statistics of network frmo which the parmeters were estimated as
# GoF check

# output file of simulated ALAAM statistics
SIMSTATS_FILE=stats_sim_gof_n500.txt

# output file of observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_n500.txt

export PYTHONPATH=../../python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time ../../python/computeALAAMstatisticsSimpleDemo.py | tee ${OBSTATS_FILE}
# TODO parse parameters for simulation from estimation output (currently 
#      hardcoded in ./runALAAMsimulateGoFexample.py  script)
time ./runALAAMsimulateGoFexample.py  | tee ${SIMSTATS_FILE}


module unload python # otherwise module load r fails
module load r
Rscript ../../R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}


