#!/bin/sh
#
# Concatenate all the job array output results into single file for 
# reading with R
#
# ADS 26 July 2023

# WARNING: overwritten
OUTFILE=stats_sim_pokec.txt

head -1 stats_sim_pokec_0.txt > ${OUTFILE}
for i in stats_sim_pokec_*.txt
do
  tail -n+2 $i >> ${OUTFILE}
done
