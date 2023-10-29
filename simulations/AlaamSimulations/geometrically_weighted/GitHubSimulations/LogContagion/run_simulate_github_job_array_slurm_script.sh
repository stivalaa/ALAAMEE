#!/bin/sh
#SBATCH --job-name="ALAAM_sim"
#SBATCH --time=0-08:00:00
#SBATCH --output=alaam_sim_github-%A_%a.out
#SBATCH --error=alaam_sim_github-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mem=500MB
#xxx SBATCH --array=0-200
#SBATCH --array=201-300

echo -n "started at: "; date
uname -a

echo SLURM_ARRAY_TASK_ID = ${SLURM_ARRAY_TASK_ID}

# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02

# run simulation from parameters and plot observed
# statistics of network from which the parmeters were estimated as
# GoF check

# output file of simulated ALAAM statistics
SIMSTATS_FILE=stats_sim_github_${SLURM_ARRAY_TASK_ID}.txt


ROOT=${HOME}
export PYTHONPATH=${ROOT}/ALAAMEE/python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time ./runALAAMsimulateGitHub.py   ${SLURM_ARRAY_TASK_ID} > ${SIMSTATS_FILE}

echo -n "ended at: "; date
