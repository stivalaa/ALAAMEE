#!/bin/sh

#SBATCH --job-name="intel_python_stochastic_approx_alaam"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-14:00:00
#SBATCH --output=alaam_sa_intel_python_karate-%j.out
#SBATCH --error=alaam_sa_intel_python_karate-%j.err

# Use the Intel Python 2.7 module
module unload python
module load python/intel27

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

# -s to make sure user libraries not used; use only the system Intel python
time python -s ../../python/runALAAMSAkarateClub.py

