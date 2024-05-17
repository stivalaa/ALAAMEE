#!/usr/bin/env python3
#
# File:    run ALAAMEEStLouisCrimeParallel.py
# Author:  Alex Stivala
# Created: September 2022
#
"""Run the simple demonstration implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. This version takes run number parameter so that
 parallel runs can be run with GNU parallel. 
 Usage:
     runALAAMEEStLouisCrimeParallel.py runNumber
"""
import getopt
import sys
from functools import partial

import estimateALAAMEE
from BipartiteGraph import MODE_A,MODE_B
from changeStatisticsALAAMbipartite import *
from changeStatisticsALAAM import changeoOc,changeo_Oc,changeo_Ob,param_func_to_label
from bipartiteALAAMsampler import bipartiteALAAMsampler

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
        'crime_bipartite.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        'crime_outcome.txt',
        'crime_binattr.txt',
        'crime_contattr.txt',
        'crime_catattr.txt',
        sampler_func = partial(bipartiteALAAMsampler, MODE_A),
        bipartite = True,
        run = runNumber,
        learningRate = 0.01 # default 0.01
    )


if __name__ == "__main__":
    main()


