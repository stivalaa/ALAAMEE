#!/bin/sh
#
# File:    build_alaamee_estimation_var_total_runs_results_tab_faster.sh
# Author:  Alex Stivala
# Created: July 2024
#
# Build table for reading into R of results of ALAAMEE estimation, varying
# total number of runs used from 1 up to 100 (assuming there are 100 
# runs present in the job output).
# 
# Usage: build_alaamee_estimation_var_total_runs_results_tab_faster.sh joboutputroot
#
# E.g.:
#   /build_alaamee_estimation_var_total_runs_results_tab.sh  /scratch/stivala/ALAAMEE_estimations_simulated_Project90/simulated_Project90
#
# Output is to stdout
#
# Uses various GNU utils options on echo, etc.

## NOTE: build_alaamee_estimation_var_total_runs_results_tab.sh is
## too slow when there are many more runs than 100, as the R script
## computeALAMEEcovariance.R has to read all the data each time, and for (e.g.)
## 500 runs this was found to be impractically slow for this use, so use
## ithis  script build_alaamee_estimation_var_total_runs_results_tab_faster.sh
## which uses new R script computeALAMEEcovariance_var_total_runs_faster.R
## where the loop is in the R script after reading the data, so is much
## more efficient.

module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

SCRIPTDIR=`dirname $0`
RSCRIPTDIR=${SCRIPTDIR}/../R

if [ $# -ne 1 ]; then
    echo "usage: $0 joboutputrootdir" >&2
    exit 1
fi

joboutputroot=$1

MAX_RUNS=500

tmpfile=`mktemp` || exit 1

echo "# Generated by: $0 $*"
echo "# At: " `date`
echo "# On: " `uname -a`
echo -e "Effect\tEstimate\tsdEstimate\tStdErr\tt-ratio\tsampleId\tnodeCount\tconvergedRuns\ttotalRuns"
for sampledir in ${joboutputroot}/sample*
do
  Rscript ${RSCRIPTDIR}/computeALAMEEcovariance_var_total_runs_faster.R --max_runs=${MAX_RUNS} ${sampledir}/theta_values_project90_giantcomponent ${sampledir}/dzA_values_project90_giantcomponent > ${tmpfile}
  if [ $? -ne 0 ]; then
    echo "ERROR: computeALAAMEEcovariance.R failed in ${sampledir}" >&2
    exit 1
  fi
  for totalRuns in `seq 1 ${MAX_RUNS}`
  do
    sampleid=`basename "${sampledir}" | sed 's/sample//g'`
    nodecount=`wc -l ${sampledir}/sample-*sim${sampleid}.txt | awk '{print $1}'`
    nodecount=`expr ${nodecount} - 1`  # less 1 for header line
    totalruns=`cat ${tmpfile} |  awk "/^MaxRuns = ${totalRuns}\$/,/^ConvergedRuns/" | fgrep -w TotalRuns | awk '{print $2}'`
    convergedruns=`cat ${tmpfile} |  awk "/^MaxRuns = ${totalRuns}\$/,/^ConvergedRuns/" | fgrep -w ConvergedRuns | awk '{print $2}'`
    # note messy special case where cannot backslash escape ! in double quotes in bash as the backslash is retaines so gives sed error, have to use single quotes
    cat ${tmpfile} |  sed -n -e "/^MaxRuns = ${totalRuns}\$/,/^TotalRuns/{//"'!p}' | tr -d '*' | fgrep -vw AcceptanceRate | fgrep -vw TotalRuns | fgrep -vw ConvergedRuns |  tr ' ' '\t'  | sed "s/\$/\t${sampleid}\t${nodecount}\t${convergedruns}\t${totalruns}/"
  done
done
rm ${tmpfile}
