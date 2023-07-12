#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=0-48:00:00
#SBATCH --output=alaam_sa_deezer-%j.out
#SBATCH --error=alaam_sa_deezer-%j.err

echo -n "started at: "; date

module load python/3.9.0

export PYTHONPATH=${HOME}/ALAAMEE/python/:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./runALAAMSAdeezer.py

echo -n "ended at: "; date
