#!/bin/sh

# Use GNU Parallel wihtout slurm etc. 

uname -a
NUM_CPUS=`nproc`
echo NUM_CPUS = $NUM_CPUS
echo -n "started at: "; date




num_waves=3
num_seeds=5
NUM_RUNS=100

echo NUM_RUNS = $NUM_RUNS
NUM_RUNS_MINUS_ONE=`expr ${NUM_RUNS} - 1`

module unload python # otherwise module load r does not work on cluster
module load r

time Rscript ../../R/snowballSampleFromExampleData.R $num_waves $num_seeds ../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt ../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt ../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt  ../data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt

module purge # otherwise cannot load python module again after module load r
module load python/3.8.5

export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs
# use with --keep-order and --line-buffer on GNU parallel

# use defulat (no --jobs option) jobs in parallel (one per CPU default)
seq 0 ${NUM_RUNS_MINUS_ONE} | parallel  --progress --joblog parallel.log --keep-order --line-buffer ../../python/runALAAMEESimpleDemoSnowballParallel.py ${num_waves} ${num_seeds}

module unload python
module load r

Rscript ../../R/plotALAAMEEResults.R theta_values_n500_kstar_simulate12750000_waves${num_waves}_seeds${num_seeds}_num6700000 dzA_values_n500_kstar_simulate12750000_waves${num_waves}_seeds${num_seeds}_num6700000


Rscript ../../R/computeALAMEEcovariance.R  theta_values_n500_kstar_simulate12750000_waves${num_waves}_seeds${num_seeds}_num6700000 dzA_values_n500_kstar_simulate12750000_waves${num_waves}_seeds${num_seeds}_num6700000

times
echo -n "ended at: "; date

