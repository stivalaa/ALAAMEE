#!/usr/bin/env python3
#
# File:    run ALAAMEEDeezerParallel.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. This version takes run number parameter so that
 parallel runs can be run with GNU parallel. 
 Usage:
     runALAAMEEDeezerParallel.py runNumber
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
        '../data/deezer_europe.net',
        [changeDensity, changeActivity, changeContagion, changeTriangleT1],
        ["Density",     "Activity",     "Contagion",     "T1"],
        ## OK GoF sim but not so good on T2,T3
        #[changeDensity, changeActivity, changeContagion, changeTriangleT1, changeTriangleT2, changeTriangleT3],
        #["Density",     "Activity",     "Contagion",     "T1",             "T2",             "T3"],
        ## Good GoF sim:
        #[changeDensity, changeActivity, changeContagion, changeTriangleT1],
        #["Density",     "Activity",     "Contagion",     "T1"],
        ## Bad GoF sim:
        #[changeDensity, changeActivity, changeContagion, changePartnerActivityTwoPath, changeIndirectPartnerAttribute],
        #["Density",     "Activity",     "Contagion",     "Alter-2Star1",               "Alter-2Star2"],
        ## Bad GoF sim:
        #[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion],
        #["Density",     "Activity",     "Two-Star",    "Three-Star",    "Contagion"],
        ## Bad GoF sim:
        #[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeContagion, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute],
        #["Density", "Activity", "Two-Star", "Three-Star", "Alter-2Star1", "Contagion", "Alter-2Star2", "Partner-Activity", "Partner-Resource"],
        ## Good GoF sim on simple model:
        #[changeDensity, changeActivity, changeContagion],
        #["Density", "Activity", "Contagion"],
        '../data/deezer_europe_target.txt',  # use gender as outcome variable
        run = runNumber
        )


if __name__ == "__main__":
    main()


