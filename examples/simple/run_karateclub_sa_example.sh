#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-04:00:00
#SBATCH --output=alaam_sa_karate-%j.out
#SBATCH --error=alaam_sa_karate-%j.err

time python ../../python/runALAAMSAkarateClub.py

