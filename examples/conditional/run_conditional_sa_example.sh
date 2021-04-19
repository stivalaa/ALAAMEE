#!/bin/sh

#SBATCH --job-name="conditional_simstochastic_approx_alaam"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-02:00:00
#SBATCH --output=alaam_conditonal_sa_simn500-%j.out
#SBATCH --error=alaam_conditonal_sa_simn500-%j.err

module load r

time Rscript ../../R/snowballSampleFromExampleData.R 2 10 ../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt ../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt ../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt  ../data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python ../../python/runALAAMSASimpleDemoSnowball.py


