#!/bin/sh

SIMSTATS_FILE=stats_sim_n500.txt

time ../../python/runALAAMsimulateSimpleDemo.py  | tee ${SIMSTATS_FILE}
Rscript ../../R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE}

