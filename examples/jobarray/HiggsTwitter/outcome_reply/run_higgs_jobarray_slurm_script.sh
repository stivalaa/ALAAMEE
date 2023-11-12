#!/bin/bash

#SBATCH --job-name="ALAAMEE_jobarray"
#SBATCH --time=0-96:00:00
#SBATCH --output=alaamee_higgs-%A_%a.out
#SBATCH --error=alaamee_higgs-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=3GB
#SBATCH --array=0-99

uname -a
echo -n "started at: "; date

echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

#module load python/3.9.0
# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02


ROOT=${HOME}/ALAAMEE
export PYTHONPATH=${ROOT}/python/:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./runALAAMEEhiggsParallel.py ${SLURM_ARRAY_TASK_ID}


echo -n "ended at: "; date
