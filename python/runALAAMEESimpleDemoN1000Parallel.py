#!/usr/bin/env python3
#
# File:    runALAAMEESimpleDemoN1000Parallel.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. This version takes run number parameter so that
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
        '../data/simulated_n1000_bin_cont/n1000_kstar_simulate12750000.txt',
        [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
        ["Density", "Activity", "Contagion", "Binary", "Continuous"],
        '../data/simulated_n1000_bin_cont/sample-n1000_bin_cont3800000.txt',
        '../data/simulated_n1000_bin_cont/binaryAttribute_50_50_n1000.txt',
        '../data/simulated_n1000_bin_cont/continuousAttributes_n1000.txt',
        run = runNumber
    )



if __name__ == "__main__":
    main()


