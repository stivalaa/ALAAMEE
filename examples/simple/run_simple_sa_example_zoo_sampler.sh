#!/bin/sh

#SBATCH --job-name="simstochastic_approx_alaam_zoo"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-02:00:00
#SBATCH --output=alaam_sa_simn500_zoo-%j.out
#SBATCH --error=alaam_sa_simn500_zoo-%j.err

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python2 ../../python/runALAAMSASimpleDemoZooSampler.py


