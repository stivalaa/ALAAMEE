#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-02:00:00
#SBATCH --output=alaam_sa_karate-%j.out
#SBATCH --error=alaam_sa_karate-%j.err

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ../../python/runALAAMSAkarateClub.py

