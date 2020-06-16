#!/bin/sh

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

SIMSTATS_FILE=stats_sim_n500.txt

time ../../python/runALAAMsimulateSimpleDemo.py  | tee ${SIMSTATS_FILE}
Rscript ../../R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE}

