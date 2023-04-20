#!/bin/sh
#
# update_estimation_dir_more_runs.sh - update estimation directories with increaesed number of runs
#
# Run on directories already built by build_estimation_dir.sh to increase
# the total number of runs by adding more runs, keeping the existing ones.
#
# Usage: update_estimation_dir_more_runs.sh output_dir
#
# output_dir is a directory already built by build_estimation_dir.sh
#  e.g.  /scratch/stivala/ALAAMEE_estimations_simulated_Project90/simulated_Project90
#
#
# Replaces the variables in the template:
#   @OLD_NUM_RUNS
#   @NEW_NUM_RUNS
#

OLD_NUM_RUNS=20
NEW_NUM_RUNS=100


SCRIPTDIR=`dirname $0`
RSCRIPTDIR=${SCRIPTDIR}/../R
TEMPLATE_DIR=${SCRIPTDIR}/templates

if [ $# -ne 1 ]; then
  echo "Usage: update_estimation_dir_more_runs.sh output_dir" >&2
  exit 1
fi
outdir=$1


for sampledir in ${data_root}/sample*
do
  sampledir=${outdir}/sample${samplenum}
  samplenum=`echo ${sampledir} | sed 's/sample//g'
  jobsuffix=${samplenum}
  template=${TEMPLATE_DIR}/run_project90simulated_parallel_slurm_script.sh.template.moreruns
  do
    mv ${sampledir}/run_project90simulated_parallel_slurm_script.sh ${sampledir}/run_project90simulated_parallel_slurm_script.sh.OLD
    cat ${template} | sed "s/@JOBSUFFIX/${jobsuffix}/g" | sed "s/@OLD_NUM_RUNS/${OLD_NUM_RUNS}/g" | sed "s/@NEW_NUM_RUNS/${NEW_NUM_RUNS}/g" > ${sampledir}/`basename ${template} .template.moreruns`
  done
done


