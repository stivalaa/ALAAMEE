#!/bin/bash

#SBATCH --job-name="get_network_data_R"
#SBATCH --ntasks=1
#SBATCH --time=0-00:01:00
#SBATCH --mem-per-cpu=4GB
#SBATCH --output=get_deezer_data-%j.out
#SBATCH --error=get_deezer_data-%j.err

echo -n "started at: "; date
uname -a

module load gcc/11.3.0 # needed by r/4.2.1
module load openmpi/4.1.4 # needed by r/4.2.1
module load r/4.2.1


time Rscript $HOME/ALAAMEE/R/convertSNAPdeezerToEEformat.R deezer_europe.zip

echo -n "ended at: "; date
