#!/bin/bash


# use the 
# run_submit_StLouisCrime_process_jobarray_slurm_script.sh
# job to submit this job and then process output with R scripts 
# on completion

#SBATCH --job-name="ALAAMEE_jobarray_parallel"
#SBATCH --time=0-02:00:00
#SBATCH --output=alaamee_StLouisCrime-%A_%a.out
#SBATCH --error=alaamee_StLouisCrime-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=200MB
#SBATCH --array=0-99


echo -n "started at: "; date
uname -a
echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

module load python/3.9.0

export PYTHONPATH=../../../../python/:${PYTHONPATH}
python3 ./runALAAMEEStLouisCrimeParallel.py ${SLURM_ARRAY_TASK_ID}


times
echo -n "ended at: "; date
