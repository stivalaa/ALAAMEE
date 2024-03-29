#!/bin/bash


# use the 
# run_submit_simple_example_process_jobarray_slurm_script.sh
# job to submit this job and then process output with R scripts 
# on completion

#SBATCH --job-name="ALAAMEE_jobarray_parallel_sim"
#SBATCH --time=0-01:00:00
#SBATCH --output=alaamee_simexample-%A_%a.out
#SBATCH --error=alaamee_simexample-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=100MB
#SBATCH --array=0-99


echo -n "started at: "; date

echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

module load python/3.9.0
python3 ../../python/runALAAMEESimpleDemoParallel.py ${SLURM_ARRAY_TASK_ID}


times
echo -n "ended at: "; date
