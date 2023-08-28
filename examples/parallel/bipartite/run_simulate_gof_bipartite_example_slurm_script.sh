#!/bin/sh
#SBATCH --job-name="gof_ALAAM"
#SBATCH --time=0-0:10:00
#SBATCH --output=gof_alaam_sim_bipartite_example-%j.out
#SBATCH --error=gof_alaam_sim_bipartite_example-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=4GB

module purge    # otherwise module load python sometimes fails
module load python/3.9.0

# run simulation from parameters and plot observed
# statistics of network from which the parmeters were estimated as
# GoF check

# output file of simulated ALAAM statistics
SIMSTATS_FILE=stats_sim_gof_inouye_bipartite.txt

# output file of observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_inouye_bipartite.txt

export PYTHONPATH=../../../python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time ./computeALAAMstatisticsBipartiteExample.py | tee ${OBSTATS_FILE}
# TODO parse parameters for simulation from estimation output (currently 
#      hardcoded in ./runALAAMsimulateGoFBipartiteExample.py  script)
time ./runALAAMsimulateGoFBipartiteExample.py  | tee ${SIMSTATS_FILE}


module unload python # otherwise module load r fails
module load r
Rscript ../../../R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}


Rscript ../../../R/plotALAAMEEsimFit.R ../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net ../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_outcome_BNA.txt sim_outcome

Rscript ../../../R/plotALAAMEEvsRandomDegreeDist.R ../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net ../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_outcome_BNA.txt sim_outcome
