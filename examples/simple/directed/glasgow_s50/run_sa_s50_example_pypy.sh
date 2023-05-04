#!/bin/sh

#SBATCH --job-name="pypy_stochastic_approx_alaam_s50"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=50MB
#SBATCH --time=0-00:10:00
#SBATCH --output=alaam_sa_s50_pypy-%j.out
#SBATCH --error=alaam_sa_s50_pypy-%j.err

echo -n "started at: "; date
uname -a

command -v module >/dev/null 2>&1 && module load python/3.9.0

export PYTHONPATH=../../../../python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs


## Using pypy3 not python3 actually take 3 times as long. So much for that...
## (On Linux [Ubuntu] Python 3.8.13 (7.3.9+dfsg-1, Apr 01 2022, 21:41:47)
##  [PyPy 7.3.9 with GCC 11.2.0])

time pypy3 runALAAMSAs50.py

echo -n "ended at: "; date
