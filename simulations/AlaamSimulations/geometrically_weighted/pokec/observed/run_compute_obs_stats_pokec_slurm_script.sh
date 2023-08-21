#!/bin/sh
#SBATCH --time=0-00:15:00
#SBATCH --output=alaam_obs_pokec-%j.out
#SBATCH --error=alaam_obs_pokec-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=8GB

echo -n "started at: "; date
uname -a


# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02

ROOT=${HOME}
export PYTHONPATH=${ROOT}/ALAAMEE/python:${PYTHONPATH}

# output file of simulated ALAAM statistics
OBSTATS_FILE=obs_stats_sim_pokec_europe.txt

time ./computeALAAMstatisticsPokec.py | tee ${OBSTATS_FILE}

echo -n "ended at: "; date
