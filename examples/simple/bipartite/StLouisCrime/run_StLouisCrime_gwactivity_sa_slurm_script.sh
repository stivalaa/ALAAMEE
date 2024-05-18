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
module load foss/2022b
module load python/3.10.8
module load numpy/1.24.2-scipy-bundle-2023.02


export PYTHONPATH=${DOCUMENTS}/USI/ALAAMEE/python/:${PYTHONPATH}
#export PYTHONPATH=../../../../python/:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./runALAAMSAStLouisCrime_gwactivity.py

echo -n "ended at: "; date
