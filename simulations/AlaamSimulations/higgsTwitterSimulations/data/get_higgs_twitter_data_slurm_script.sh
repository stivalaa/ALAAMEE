#!/bin/bash

#SBATCH --job-name="get_network_data_R"
#SBATCH --ntasks=1
#SBATCH --time=0-00:30:00
#SBATCH --mem-per-cpu=4GB
#SBATCH --output=get_higgs_data-%j.out
#SBATCH --error=get_higgs_data-%j.err

echo -n "started at: "; date
uname -a

module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1

time Rscript ../../../../R/convertSNAPhiggsTwitterToALAAMEEFormat.R 

echo -n "ended at: "; date
