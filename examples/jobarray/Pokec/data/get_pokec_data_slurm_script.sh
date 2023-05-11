#!/bin/bash

#SBATCH --job-name="get_network_data_R"
#SBATCH --ntasks=1
#SBATCH --time=0-01:00:00
#SBATCH --mem-per-cpu=8GB
#SBATCH --output=get_pokec_data-%j.out
#SBATCH --error=get_pokec_data-%j.err

module load r

echo -n "started at: "; date
uname -a

time Rscript $HOME/ALAAMEE/R/convertSNAPpokecToALAAMEEFormat.R 1000 
##all nodes, does not converge on alaam (like ergm): time Rscript $HOME/ALAAMEE/R/convertSNAPpokecToALAAMEEFormat.R 

echo -n "ended at: "; date
