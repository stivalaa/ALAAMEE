#!/bin/sh
#SBATCH --job-name="ALAAM_obs"
#SBATCH --time=0-02:35:00
#SBATCH --output=alaam_obs_higgs_outcome_reply-%j.out
#SBATCH --error=alaam_obs_higgs_outcome_reply-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=4GB

echo -n "started at: "; date
uname -a


# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02

ROOT=${HOME}
export PYTHONPATH=${ROOT}/ALAAMEE/python:${PYTHONPATH}

# output file of simulated ALAAM statistics
OBSTATS_FILE=obs_stats_sim_higgs_europe_outcome_reply.txt

time python3 ./computeALAAMstatisticsHiggsOutcomeReply.py | tee ${OBSTATS_FILE}

echo -n "ended at: "; date
