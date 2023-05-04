#!/bin/sh

#SBATCH --job-name="simstochastic_approx_alaam"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-02:00:00
#SBATCH --output=alaam_sa_simn1000-%j.out
#SBATCH --error=alaam_sa_simn1000-%j.err

command -v module >/dev/null 2>&1 && module load python/3.9.0

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ../../python/runALAAMSASimpleDemoN1000.py


