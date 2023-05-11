#!/usr/bin/env python3
#
# File:    run ALAAMEEpokecParallel.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. This version takes run number parameter so that
 parallel runs can be run with GNU parallel. 
 Usage:
     runALAAMEEpokecParallel.py runNumber
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
        '../data/soc-pokec-relationships-undirected.net',
        [changeDensity, changeContagion, partial(changeoOc, "age")],
        ["Density", "Contagion", "age_oOc"],
        ## Only 8/20 converge on estimation:
        #[changeDensity, changeContagion, changeTriangleT1, changeTriangleT2, partial(changeoOc, "age")],
        #["Density", "Contagion", "T1", "T2",  "age_oOc"],
        ## Bad GoF sim on T1 (only):
        ## Only 11/20 converge on estimation:
        #[changeDensity, changeContagion, changeTriangleT1, changeTriangleT2, changeTriangleT3, partial(changeoOc, "age")],
        #["Density", "Contagion", "T1", "T2", "T3", "age_oOc"],
        ## Bad GoF sim on T1 (only):
        #[changeDensity, changeContagion, changeTriangleT1, partial(changeoOc, "age")],
        #["Density", "Contagion", "T1", "age_oOc"],
        ## Bad GoF sim:
        #[changeDensity, changeContagion, changeTwoStar, partial(changeoOc, "age")],
        #["Density", "Contagion", "Two-Star", "age_oOc"],
        ## Bad GoF sim:
        #[changeDensity, changeContagion, changeIndirectedPartnerAttribute, partial(changeoOc, "age")],
        #["Density", "Contagion", "Alter-2Star2", "age_oOc"],
        ## Bad GoF sim on Activity and Contagion:
        #[changeDensity, changeActivity, changeContagion, partial(changeoOc, "age")],
        #["Density", "Activity", "Contagion", "age_oOc"],
        ## GoF sim OK, not great on contagion (t-ratio -1.64):
        #[changeDensity, changeContagion, partial(changeoOc, "age")],
        #["Density", "Contagion", "age_oOc"],
        ## very bad GoF sim on all parameters:
        #[changeDensity,  changeActivity, changeTwoStar, changeThreeStar, partial(changeoOc, "age"), partial(changeoO_Osame, "region")],
        #["Density", "Activity", "Two-Star", "Three-Star" ,"age_oOc", "region_oO_Osame"],
        ## Bad GoF sim on contagion and region:
        #[changeDensity, changeContagion, partial(changeoOc, "age"), partial(changeoO_Osame, "region")],
        #["Density", "Contagion", "age_oOc", "region_oO_Osame"],
        ## Sim GoF OK (not ideal on region perhaps, t-ratio=-1.8)
        #[changeDensity, partial(changeoOc, "age"), partial(changeoO_Osame, "region")],
        #["Density", "age_oOc", "region_oO_Osame"],
        ## Bad GoF sim on activity and region:
        #[changeDensity, changeActivity, partial(changeoOc, "age"), partial(changeoO_Osame, "region")],
        #["Density", "Activity", "age_oOc", "region_oO_Osame"],
        ## Bad GoF sim on activity and contagion and region (same as first try with age):
        #[changeDensity, changeActivity, changeContagion],
        #["Density", "Activity", "Contagion"],
        ## Bad GoF sim on activity and contagion and region:
        #[changeDensity, changeActivity, changeContagion,  partial(changeoO_Osame, "region")],
        #["Density", "Activity", "Contagion",  "region_oO_Osame"],
        ## Does not converge:
        #[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeContagion, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute,   partial(changeoOc, "age"), partial(changeoO_Osame, "region")],
        #["Density", "Activity", "Two-Star", "Three-Star", "Alter-2Star1", "Contagion", "Alter-2Star2", "Partner-Activity", "Partner-Resource",  "age_oOc", "region_oO_Osame"],
        '../data/soc-pokec-binattr.txt',  # use male as outcome variable
        #does not converge:'../data/soc-pokec-outcome.txt',  # use public as outcome variable
        None, #'../data/soc-pokec-binattr.txt',
        '../data/soc-pokec-contattr.txt',
        '../data/soc-pokec-catattr.txt',
        run = runNumber
        )


if __name__ == "__main__":
    main()


