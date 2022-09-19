#!/bin/sh

#SBATCH --job-name="simstochastic_approx_alaam_bipartite"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=100M
#SBATCH --time=0-00:40:00
#SBATCH --output=alaam_sa_inouye-%j.out
#SBATCH --error=alaam_sa_inouye-%j.err

echo -n "started at: "; date
uname -a

module purge # otherwise sometimes module load fails
module load python/3.9.0

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ../../python/runALAAMSABipartiteSimpleDemo.py


echo -n "ended at: "; date
