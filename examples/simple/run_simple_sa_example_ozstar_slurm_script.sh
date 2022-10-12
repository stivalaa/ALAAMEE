#!/bin/sh

#SBATCH --job-name="simstochastic_approx_alaam"
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-01:00:00
#SBATCH --output=alaam_sa_simn500-%j.out
#SBATCH --error=alaam_sa_simn500-%j.err

echo -n "started at: "; date
uname -a

module load numpy/1.22.3-python-3.10.4

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ../../python/runALAAMSASimpleDemo.py

echo -n "ended at: "; date
