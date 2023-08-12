#!/bin/bash


# use the 
# run_submit_g_process_jobarray_slurm_script.sh
# job to submit this job and then process output with R scripts 
# on completion

#SBATCH --job-name="ALAAMEE_jobarray_parallel"
#SBATCH --time=0-03:00:00
#SBATCH --output=alaamee_pokec-%A_%a.out
#SBATCH --error=alaamee_pokec-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=4GB
#SBATCH --array=0-99


echo -n "started at: "; date

echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

module load python/3.9.0

export PYTHONPATH=${HOME}/ALAAMEE/python/:${PYTHONPATH}
python3 ./runALAAMEEpokecParallel.py ${SLURM_ARRAY_TASK_ID}


times
echo -n "ended at: "; date
