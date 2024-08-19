#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam_highschool_gender_more_igraph"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=500MB
#SBATCH --time=0-01:00:00
#SBATCH --output=alaam_sa_highschool_gender_more_igraph-%j.out
#SBATCH --error=alaam_sa_highschool_gender_more_igraph-%j.err

echo -n "started at: "; date
uname -a

export PYTHONPATH=../../../../python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 runALAAMSAhighschool_gender_more_igraph.py

echo -n "ended at: "; date
