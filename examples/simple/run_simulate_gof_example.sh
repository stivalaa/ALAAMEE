#!/bin/sh

# example to run simulation from parameters and plot observed
# statistics (of network sampled from ALAAM with those parameters - in actual
# use would be network from which the parmeters were estimated) as
# GoF check

# output file of simulated ALAAM statistics
SIMSTATS_FILE=stats_sim_gof_n500.txt

# output file of observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_n500.txt

time ../../python/computeALAAMstatisticsSimpleDemo.py | tee ${OBSTATS_FILE}
time ../../python/runALAAMsimulateSimpleDemo.py  | tee ${SIMSTATS_FILE}
Rscript ../../R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}


