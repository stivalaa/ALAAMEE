#!/bin/bash

#SBATCH --job-name="get_network_data_R"
#SBATCH --ntasks=1
#SBATCH --time=0-00:01:00
#SBATCH --mem-per-cpu=4GB
#SBATCH --output=get_github_data-%j.out
#SBATCH --error=get_github_data-%j.err

module load r

echo -n "started at: "; date
uname -a

time Rscript $HOME/ALAAMEE/R/convertSNAPgithubToEEformat.R git_web_ml.zip

echo -n "ended at: "; date
