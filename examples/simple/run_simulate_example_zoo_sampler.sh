#!/bin/sh

SIMSTATS_FILE=stats_sim_n500_zoo.txt

time ../../python/runALAAMsimulateSimpleDemoZooSampler.py  | tee ${SIMSTATS_FILE}
Rscript ../../R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE}

