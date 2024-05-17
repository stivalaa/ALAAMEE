#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam_harmonic"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=500MB
#SBATCH --time=0-04:00:00
#SBATCH --output=alaam_sa_seierstad_harmonic-%j.out
#SBATCH --error=alaam_sa_seierstad_harmonic-%j.err

echo -n "started at: "; date
uname -a

command -v module >/dev/null 2>&1 && module purge
# module version numbers are required on OzStar (Ngarrgu Tindebeek)
command -v module >/dev/null && module load foss/2022b
command -v module >/dev/null && module load python/3.10.8
command -v module >/dev/null && module load numpy/1.24.2-scipy-bundle-2023.02

#export PYTHONPATH=${DOCUMENTS}/USI/ALAAMEE/python/:${PYTHONPATH}
export PYTHONPATH=${HOME}/ALAAMEE/python/:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

ESTIM_FILE=estimation_sa_seierstad_directors_bipartite_harmonic.txt

if [ -f ${ESTIM_FILE} ]; then
  mv ${ESTIM_FILE} ${ESTIM_FILE}.OLD
fi

time python3 ./runALAAMSASeierstad_harmonic.py | tee ${ESTIM_FILE}

echo -n "ended at: "; date

