#!/bin/bash

# Submit job array to do parallel ALAMEE runs
# and another job to process the output with R scripts, waiting
# for the parallel jobs to finish first

module purge # otherwise will fail if R module is loaded

jobid=$(sbatch --parsable run_deezer_jobarray_slurm_script.sh)

echo ${jobid}

sbatch --dependency=afterok:${jobid} run_deezer_R_scripts_slurm_script.sh

