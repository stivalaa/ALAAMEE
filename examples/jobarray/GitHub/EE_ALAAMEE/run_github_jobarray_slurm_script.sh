#!/bin/bash


# use the 
# run_submit_github_process_jobarray_slurm_script.sh
# job to submit this job and then process output with R scripts 
# on completion

#SBATCH --job-name="ALAAMEE_jobarray_parallel"
#SBATCH --time=0-00:30:00
#SBATCH --output=alaamee_Github-%A_%a.out
#SBATCH --error=alaamee_Github-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=1GB
#SBATCH --array=0-99
#SBATCH --partition=slim


echo -n "started at: "; date

echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

#module load python/3.9.0
# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02

export PYTHONPATH=${HOME}/ALAAMEE/python/:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

python3 ./runALAAMEEGithubParallel.py ${SLURM_ARRAY_TASK_ID}


times
echo -n "ended at: "; date
