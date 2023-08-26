#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam_highschool_class_gw_more"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=500MB
#SBATCH --time=0-02:00:00
#SBATCH --output=alaam_sa_highschool_class_gw_more-%j.out
#SBATCH --error=alaam_sa_highschool_class_gw_more-%j.err

echo -n "started at: "; date
uname -a

command -v module >/dev/null 2>&1 && module load python/3.9.0

export PYTHONPATH=../../../../python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 runALAAMSAhighschool_class_gw_more.py

echo -n "ended at: "; date
