#!/bin/sh

#SBATCH --job-name="stochastic_approx_alaam_s50"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=500MB
#SBATCH --time=0-00:10:00
#SBATCH --output=alaam_sa_s50-%j.out
#SBATCH --error=alaam_sa_s50-%j.err

echo -n "started at: "; date
uname -a

command -v module >/dev/null 2>&1 && module load python/3.9.0

export PYTHONPATH=../../../../python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 runALAAMSAs50.py

command -v module >/dev/null 2>&1 && module load gcc/11.3.0 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load openmpi/4.1.4 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load r/4.2.1

## Python actually doing estimation and GoF only needs 50MB but R needs much more
Rscript ../../../../R/plotSimulationDiagnostics.R  s50_gof_stats.txt s50_obs_stats.txt

echo -n "ended at: "; date
