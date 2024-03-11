#!/bin/bash

# Submit job array to do parallel ALAMEE runs
# and another job to process the output with R scripts, waiting
# for the parallel jobs to finish first, and also do simulation-based GoF test
# (which requires output of the estimation processing R scripts)

module purge # otherwise will fail if R module is loaded

jobid=$(sbatch --parsable run_gemsec_deezer_hr_jobarray_slurm_script.sh)
echo ${jobid}
R_jobid=$(sbatch --parsable --dependency=afterok:${jobid} run_gemsec_deezer_hr_R_scripts_slurm_script.sh)
echo ${R_jobid}
sbatch --dependency=afterok:${R_jobid} run_simulate_gof_gemsec_deezer_hr_slurm_script.sh

