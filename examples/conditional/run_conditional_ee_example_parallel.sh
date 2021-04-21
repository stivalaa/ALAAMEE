#!/bin/sh

# Use GNU Parallel wihtout slurm etc. just using nproc to get number of cores

uname -a
NUM_CPUS=`nproc`
echo NUM_CPUS = $NUM_CPUS
echo -n "started at: "; date

CPUS_MINUS_ONE=`expr ${NUM_CPUS} - 1`


num_waves=2
num_seeds=10

time Rscript ../../R/snowballSampleFromExampleData.R $num_waves $num_seeds ../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt ../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt ../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt  ../data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt


seq 0 ${CPUS_MINUS_ONE} | parallel -j ${NUM_CPUS} --progress --joblog parallel.log ../../python/runALAAMEESimpleDemoSnowballParallel.py ${num_waves} ${num_seeds}

Rscript ../../R/plotALAAMEEResults.R theta_values_n500_kstar_simulate12750000_waves${num_waves}_seeds${num_seeds}_num6700000 dzA_values_n500_kstar_simulate12750000_waves${num_waves}_seeds${num_seeds}_num6700000


Rscript ../../R/computeALAMEEcovariance.R  theta_values_n500_kstar_simulate12750000_waves${num_waves}_seeds${num_seeds}_num6700000 dzA_values_n500_kstar_simulate12750000_waves${num_waves}_seeds${num_seeds}_num6700000

times
echo -n "ended at: "; date

