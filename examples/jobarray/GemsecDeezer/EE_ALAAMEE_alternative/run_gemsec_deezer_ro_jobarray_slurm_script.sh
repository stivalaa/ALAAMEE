#!/bin/bash


# use the 
# run_submit_gemsec_deezer_ro_process_jobarray_slurm_script.sh
# job to submit this job and then process output with R scripts 
# on completion

#SBATCH --job-name="ALAAMEE_RO_jobarray_parallel"
#SBATCH --time=0-02:00:00
#SBATCH --output=alaamee_GEMSEC_Deezer_RO-%A_%a.out
#SBATCH --error=alaamee_GEMSEC_Deezer_RO-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=100MB
#SBATCH --array=0-199


echo -n "started at: "; date

echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02


export PYTHONPATH=../../../..//python/:${PYTHONPATH}
python3 ./runALAAMEEGemsecDeezerROParallel.py ${SLURM_ARRAY_TASK_ID}


times
echo -n "ended at: "; date
