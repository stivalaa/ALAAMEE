#!/bin/sh

# get elapsed time in minutes and make histogram, saving times in minutes to file

#WARNING: overwritten
outfile=jobtimes.txt

~/ALAAMEE/scripts/getbashtimes.sh  alaamee_Deezer-2260969_*.out | awk '{print $1 / 60}'  >  ${outfile}

cat ${outfile} | histogram.py
