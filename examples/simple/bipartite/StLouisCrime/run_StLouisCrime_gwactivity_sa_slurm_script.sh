#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam_StLouisCrime_gwactivity"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=500MB
#SBATCH --time=0-8:00:00
#SBATCH --output=alaam_sa_stlouiscrime_gwactivity-%j.out
#SBATCH --error=alaam_sa_stlouiscrime_gwactivity-%j.err

echo -n "started at: "; date
uname -a

# module version numbers are required on OzStar (Ngarrgu Tindebeek)
command -v module >/dev/null 2>&1 && module load foss/2022b
command -v module >/dev/null 2>&1 && module load python/3.10.8
command -v module >/dev/null 2>&1 && module load numpy/1.24.2-scipy-bundle-2023.02

export PYTHONPATH=../../../../python/:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./runALAAMSAStLouisCrime_gwactivity.py

echo -n "ended at: "; date
