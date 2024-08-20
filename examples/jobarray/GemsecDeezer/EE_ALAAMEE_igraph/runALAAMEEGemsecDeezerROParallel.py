#!/usr/bin/env python3
#
# File:    run runALAAMEEGemsecDeezerROParallel.py
# Author:  Alex Stivala
# Created: August 2024
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. This version takes run number parameter so that
 parallel runs can be run with GNU parallel. 
 Usage:
     runrunALAAMEEGemsecDeezerROParallel.py runNumber

 This version uses the data in an igraph object rather than 
 reading the network and data inside ALAAMEE functions.
"""
import getopt
import sys
from functools import partial
import igraph

import  estimateALAAMEE
from changeStatisticsALAAM import param_func_to_label

from model import param_func_list
from readData import read_ro_data


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

    g = read_ro_data()
    estimateALAAMEE.run_ee(g,  # Graph object with node attributes
        g.binattr['outcome'],  # outcome binary attribute vector
        "deezer_ro_friendship",# theta_values_<name>_* and dzA_values_<name>_*
        param_func_list,       # model parameters
        [param_func_to_label(f) for f in param_func_list], # labels for params
        run = runNumber,       # parallel run number from job array
        learningRate = 0.01    # learning rate r for EE algorithm
        )


if __name__ == "__main__":
    main()


