#!/bin/sh

#SBATCH --job-name="simstochastic_approx_alaam_directed"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-00:30:00
#SBATCH --output=alaam_sa_directed-%j.out
#SBATCH --error=alaam_sa_directed-%j.err

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ../../../python/runALAAMSASimpleDemoDirected.py
