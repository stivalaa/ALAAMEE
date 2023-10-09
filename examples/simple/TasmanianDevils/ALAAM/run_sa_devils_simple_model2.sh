#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam_devils_simple_model2"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=40MB
#SBATCH --time=0-00:10:00
#SBATCH --output=alaam_sa_devils_simple_model2-%j.out
#SBATCH --error=alaam_sa_devils_simple_model2-%j.err

echo -n "started at: "; date
uname -a

command -v module >/dev/null 2>&1 && module load python/3.9.0

export PYTHONPATH=${DOCUMENTS}/USI/ALAAMEE/python:${PYTHONPATH}
#export PYTHONPATH=../../../python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 runALAAMSAdevilsSimpleModel2.py

echo -n "ended at: "; date
