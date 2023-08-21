#!/usr/bin/env python3
#
# File:    run ALAAMEEhiggsParallel.py
# Author:  Alex Stivala
# Created: August 2023
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. This version takes run number parameter so that
 parallel runs can be run with GNU parallel. 
 Usage:
     runALAAMEEhiggsParallel.py runNumber
"""
import getopt
import sys
from functools import partial

import  estimateALAAMEE
from changeStatisticsALAAM import *
from changeStatisticsALAAMdirected import *
from model import param_func_list


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
        '../data/higgs_social.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        '../data/higgs_reply_active.txt',
        run = runNumber,
        learningRate = 0.001,
        directed = True
        )


if __name__ == "__main__":
    main()


