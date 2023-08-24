#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam_highschool_gender"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=50MB
#SBATCH --time=0-00:10:00
#SBATCH --output=alaam_sa_highschool_gender-%j.out
#SBATCH --error=alaam_sa_highschool_gender-%j.err

echo -n "started at: "; date
uname -a

command -v module >/dev/null 2>&1 && module load python/3.9.0

export PYTHONPATH=../../../../python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 runALAAMSAhighschool_gender.py

echo -n "ended at: "; date
