#!/bin/sh
#
# build_estimation_dir.sh - build estimation directories for simualted ALAAM data
#
# This involves copying the network and attribute fies, convertingthem from
# IPNet format to ALAAMEE format, i.e. converting ajadcency matrix to Pajek
# format edge list, and replacing Pajel .clu outcome variable
# (*vertices as header line) to ALAAMEE/EstimNEtDirected format with
# attribute name as header line.
#
# ALso create slurm and Python scripts from templates directory
# by replacing the following:
#
#   @OUTCOMEFILE
#   @JOBSUFFIX
#   @NUM_RUNS
#
# Usage: build_estimation_dir.sh data_root
#
# data_root is source of the input simulation data
#  e.g. ~/Project90_alaam_data/simulated_project90/
#
# Creates directories in cwd
#

module load r

NUM_RUNS=20


SCRIPTDIR=`dirname $0`
RSCRIPTDIR=${SCRIPTDIR}/../R
TEMPLATE_DIR=${SCRIPTDIR}/templates

if [ $# -ne 1 ]; then
  echo "Usage: build_estimation_dir.sh data_root" >&2
  exit 1
fi
data_root=$1


outdir=./`basename ${data_root}`
mkdir ${outdir}

cp -p ${data_root}/parameter-project90_sim.txt ${outdir}

Rscript ${RSCRIPTDIR}/convertMatrixToEdgelist.R < ${data_root}/project90_giantcomponent_adjmatrix.txt > ${outdir}/project90_giantcomponent.net

binattr=binaryAttribute_50_50_n4430.txt
echo "binattr" > ${outdir}/${binattr}
cat ${data_root}/${binattr} >> ${outdir}/${binattr}

contattr=continuousAttributes_n4430.txt
echo "contattr" > ${outdir}/${contattr}
cat ${data_root}/${contattr} >> ${outdir}/${contattr}

for outcomeclu in ${data_root}/sample-project90_sim*.clu
do
  samplenum=`echo ${outcomeclu} | sed "s!${data_root}/sample-project90_sim!!g" | sed 's/[.]clu//g'`
  sampledir=${outdir}/sample${samplenum}
  outcomefilename=`basename ${outcomeclu} .clu`.txt
  outcomefile=${sampledir}/${outcomefilename}
  jobsuffix=${samplenum}
  mkdir ${sampledir}
  echo "outcome" > ${outcomefile}
  tail -n+2 ${outcomeclu} >> ${outcomefile}
  for template in ${TEMPLATE_DIR}/runALAAMEEproject90simulatedParallel.py.template ${TEMPLATE_DIR}/run_project90sim_R_scripts_slurm_script.sh.template ${TEMPLATE_DIR}/run_project90simulated_parallel_slurm_script.sh.template ${TEMPLATE_DIR}/run_submit_project90simulated_parallel_slurm_script.sh.template
  do
    cat ${template} | sed "s/@OUTCOMEFILE/${outcomefilename}/g" | sed "s/@JOBSUFFIX/${jobsuffix}/g" | sed "s/@NUM_RUNS/${NUM_RUNS}/g" > ${sampledir}/`basename ${template} .template`
  done
done


