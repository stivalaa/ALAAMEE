#!/bin/sh

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

SIMSTATS_FILE=stats_sim_n500_zoo.txt

time ../../python/runALAAMsimulateSimpleDemoZooSampler.py  | tee ${SIMSTATS_FILE}
Rscript ../../R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE}

