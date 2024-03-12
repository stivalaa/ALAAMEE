#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam_gemsec_hu"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=500MB
#SBATCH --time=0-48:00:00
#SBATCH --output=alaam_sa_deezer_hu-%j.out
#SBATCH --error=alaam_sa_deezer_hu-%j.err

echo -n "started at: "; date
uname -a

# module version numbers are required on OzStar (Ngarrgu Tindebeek)
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02


export PYTHONPATH=../../../../python/:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./runALAAMSAgemsecDeezerHU.py

echo -n "ended at: "; date
