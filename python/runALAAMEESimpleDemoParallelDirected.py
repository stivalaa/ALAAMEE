#!/usr/bin/env python3
#
# File:    runALAAMEESimpleDemoParallelDirected.py
# Author:  Alex Stivala
# Created: Februrary 2022
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters for a directed network.
 This version takes run number parameter so that
 parallel runs can be run with GNU parallel. 
 Usage:
     runALAAMEESimpleDemoParallel.py runNumber

  E.g. for 16 parallel runs:

  seq 0 15 |  parallel -j 16 --progress --joblog parallel.log runALAAMEESimpleDemoParallel.py


 Citation for GNU parallel:

  O. Tange (2018): GNU Parallel 2018, Mar 2018, ISBN 9781387509881,
  DOI https://doi.org/10.5281/zenodo.11460

"""
import getopt
import sys
from functools import partial
import  estimateALAAMEE
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity



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
        '../../data/directed/HighSchoolFriendship/highschool_friendship_arclist.net',
        [changeDensity, changeSender, changeReceiver, changeContagion],
        ["Density", "Sender", "Receiver", "Contagion"],
        outcome_bin_filename = '../../data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt',
        EEiterations = 10000,
        run = runNumber,
        directed = True
    )


if __name__ == "__main__":
    main()


