#!/bin/sh
#SBATCH --job-name="gof_ALAAM"
#SBATCH --time=0-00:10:00
#SBATCH --output=gof_alaam_sim_highschool-%j.out
#SBATCH --error=gof_alaam_sim_highschool-%j.err
#SBATCH --ntasks=1
#SBATCH --mem=4GB

echo -n "started at: "; date
uname -a

command -v module >/dev/null 2>&1 && module load foss/2022b
command -v module >/dev/null 2>&1 && module load python/3.10.8
command -v module >/dev/null 2>&1 && module load numpy/1.24.2-scipy-bundle-2023.02

command -v module >/dev/null 2>&1 && module load gcc/11.3.0 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load openmpi/4.1.4 # needed by r/4.2.1
command -v module >/dev/null 2>&1 && module load r/4.2.1
    

# run simulation from parameters and plot observed
# statistics of network from which the parmeters were estimated as
# GoF check

# output file of observed ALAAM statistics
OBSTATS_FILE=obs_stats_sim_highschool.txt

ROOT=../../../../
export PYTHONPATH=${ROOT}/python:${PYTHONPATH}
export PYTHONUNBUFFERED=1    # unbuffered stdout to see progress as it runs

time python3 ./computeALAAMstatisticsHighschool.py | tee ${OBSTATS_FILE}

for gwsender in estimated zero negative positive
do
    # output file of simulated ALAAM statistics
    SIMSTATS_FILE=stats_sim_gof_highschool_${gwsender}.txt
    
    time python3 ./runALAAMsimulateGoFHighschool.py ${gwsender}  | tee ${SIMSTATS_FILE}
    
    Rscript ${ROOT}/R/plotSimulationDiagnostics.R  ${SIMSTATS_FILE} ${OBSTATS_FILE}
    
    Rscript ${ROOT}/R/plotALAAMEEsimFit.R ../../../data/directed/HighSchoolFriendship/highschool_friendship_arclist.net ../../../data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt sim_outcome_${gwsender}
    
    Rscript ${ROOT}/R/plotALAAMEEvsRandomDegreeDist.R  ../../../data/directed/HighSchoolFriendship/highschool_friendship_arclist.net ../../../data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt sim_outcome_${gwsender}
done

times
echo -n "started at: "; date
