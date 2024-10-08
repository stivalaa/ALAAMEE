#!/bin/sh

#SBATCH --job-name="conditional_simstochastic_approx_alaam"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-02:00:00
#SBATCH --output=alaam_conditonal_sa_simn500-%j.out
#SBATCH --error=alaam_conditonal_sa_simn500-%j.err


module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

num_waves=2
num_seeds=10

time Rscript ../../R/snowballSampleFromExampleData.R $num_waves $num_seeds ../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt ../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt ../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt  ../data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt


export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ../../python/runALAAMSASimpleDemoSnowball.py $num_waves $num_seeds


