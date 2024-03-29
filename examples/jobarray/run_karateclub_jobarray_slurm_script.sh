#!/bin/bash


# use the 
# run_submit_karateclub_process_jobarray_slurm_script.sh
# job to submit this job and then process output with R scripts 
# on completion

#SBATCH --job-name="ALAAMEE_jobarray_parallel_sim"
#SBATCH --time=0-02:00:00
#SBATCH --output=alaamee_karate-%A_%a.out
#SBATCH --error=alaamee_karate-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=100MB
#SBATCH --array=0-99


echo -n "started at: "; date

echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

module load python/3.9.0
python3 ../../python/runALAAMEEkarateClubParallel.py ${SLURM_ARRAY_TASK_ID}


times
echo -n "ended at: "; date
