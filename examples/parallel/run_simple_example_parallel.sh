#!/bin/bash

# Use GNU Parallel wihtout slurm etc. just using nproc to get number of cores

uname -a
NUM_CPUS=`nproc`
echo NUM_CPUS = $NUM_CPUS
echo -n "started at: "; date

CPUS_MINUS_ONE=`expr ${NUM_CPUS} - 1`

seq 0 ${CPUS_MINUS_ONE} | parallel -j ${NUM_CPUS} --progress --joblog parallel.log ../../python/runALAAMEESimpleDemoParallel.py

Rscript ../../R/plotALAAMEEResults.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000


Rscript ../../R/computeALAMEEcovariance.R theta_values_n500_kstar_simulate12750000 dzA_values_n500_kstar_simulate12750000

times
echo -n "ended at: "; date
