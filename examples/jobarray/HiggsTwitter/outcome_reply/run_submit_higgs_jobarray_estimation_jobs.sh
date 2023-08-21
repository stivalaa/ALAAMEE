#!/bin/bash

jobid=$(sbatch --parsable run_higgs_jobarray_slurm_script.sh)
echo ${jobid}
sbatch --dependency=afterok:${jobid} run_higgs_R_scripts_slurm_script.sh
