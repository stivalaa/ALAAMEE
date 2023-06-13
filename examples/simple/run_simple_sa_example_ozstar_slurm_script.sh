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

# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ../../python/runALAAMSASimpleDemo.py

echo -n "ended at: "; date
