#!/bin/bash

# Submit job array to do parallel ALAMEE runs
# and another job to process the output with R scripts, waiting
# for the parallel jobs to finish first

jobid=$(sbatch --parsable run_StLouisCrime_jobarray_slurm_script.sh)

echo ${jobid}

sbatch --dependency=afterok:${jobid} run_StLouisCrime_R_scripts_slurm_script.sh

