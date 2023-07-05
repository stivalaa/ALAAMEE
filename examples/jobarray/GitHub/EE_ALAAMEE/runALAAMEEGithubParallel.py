#!/usr/bin/env python3
#
# File:    run ALAAMEEGithubParallel.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. This version takes run number parameter so that
 parallel runs can be run with GNU parallel. 
 Usage:
     runALAAMEEGithubParallel.py runNumber
"""
import getopt
import sys
from functools import partial

import  estimateALAAMEE
from changeStatisticsALAAM import *


def usage(progname):
    """
    print usage msg and exit
    """
    sys.stderr.write("usage: " + progname + " runNumber\n")
    sys.exit(1)


def main():
    """
    See usage message in module header block
    """
    directed = False
    try:
        opts,args = getopt.getopt(sys.argv[1:], "")
    except:
        usage(sys.argv[0])
    for opt,arg in opts:
        usage(sys.argv[0])

    if len(args) != 1:
        usage(sys.argv[0])

    runNumber = int(args[0])

    estimateALAAMEE.run_on_network_attr(
        '../data/musae_git.net',
        [changeDensity, changeActivity,   changeContagion],
        ["Density",     "Activity",       "Contagion"],
        ### with learningRate = 0.001:
        ## Does not converge:
        #[changeDensity, changeActivity, changeTwoStar,  changeContagion],
        #["Density",     "Activity",     "Two-Star",    "Contagion"],
        ### with default learningRate = 0.01:
        ## Bad GoF sim:
        #[changeDensity, changeActivity,   changeContagion],
        #["Density",     "Activity",       "Contagion"],
        ## Does not converge:
        #[changeDensity, changeActivity, changeTwoStar,  changeContagion],
        #["Density",     "Activity",     "Two-Star",    "Contagion"],
        ## Does not converge:
        #[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion],
        #["Density",     "Activity",     "Two-Star",    "Three-Star",   "Contagion"],
        #[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeContagion, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute],
        #["Density", "Activity", "Two-Star", "Three-Star", "Alter-2Star1", "Contagion", "Alter-2Star2", "Partner-Activity", "Partner-Resource"],
        '../data/musae_git_target.txt',  # use target developer type as outcome variable
        run = runNumber,
        learningRate = 0.001,
        )


if __name__ == "__main__":
    main()


