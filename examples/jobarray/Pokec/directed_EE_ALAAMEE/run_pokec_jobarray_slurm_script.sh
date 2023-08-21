#!/bin/bash


# use the 
# run_submit_g_process_jobarray_slurm_script.sh
# job to submit this job and then process output with R scripts 
# on completion

#SBATCH --job-name="ALAAMEE_jobarray_parallel"
#SBATCH --time=0-2:00:00
#SBATCH --output=alaamee_pokec-%A_%a.out
#SBATCH --error=alaamee_pokec-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=8GB
#SBATCH --array=0-99


echo -n "started at: "; date

echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02


export PYTHONPATH=${HOME}/ALAAMEE/python/:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runsa

time python3 ./runALAAMEEpokecParallel.py ${SLURM_ARRAY_TASK_ID}


echo -n "ended at: "; date
