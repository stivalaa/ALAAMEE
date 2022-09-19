#!/usr/bin/env python3
#
# File:    runALAAMEEBipartiteDemoParallel.py
# Author:  Alex Stivala
# Created: August 2022
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. This version takes run number parameter so that
 parallel runs can be run with GNU parallel. 
 Usage:
     runALAAMEEBipartiteDemoParallel.py runNumber

  E.g. for 16 parallel runs:

  seq 0 15 |  parallel -j 16 --progress --joblog parallel.log runALAAMEEBipartiteDemoParallel.py


 Citation for GNU parallel:

  [from --help]

  O. Tange (2018): GNU Parallel 2018, Mar 2018, ISBN 9781387509881,
  DOI https://doi.org/10.5281/zenodo.11460

  [from --citation]:

  @software{tange_2021_4628277,
      author       = {Tange, Ole},
      title        = {GNU Parallel 20210322 ('2002-01-06')},
      month        = Mar,
      year         = 2020,
      note         = {{GNU Parallel is a general parallelizer to run
                       multiple serial command line programs in parallel
                       without changing them.}},
      publisher    = {Zenodo},
      doi          = {10.5281/zenodo.4628277},
      url          = {https://doi.org/10.5281/zenodo.4628277}
}


"""
import getopt
import sys
from functools import partial
import  estimateALAAMEE
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
from bipartiteALAAMsampler import bipartiteALAAMsampler
from changeStatisticsALAAMbipartite import *


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

    estimateALAAMEE.run_on_network_attr('../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net',
            [partial(changeBipartiteDensity, MODE_A),
             partial(changeBipartiteActivity, MODE_A),
             partial(changeBipartiteEgoTwoStar, MODE_A),
             partial(changeBipartiteAlterTwoStar1,MODE_A),
             partial(changeBipartiteAlterTwoStar2,MODE_A),
             partial(changeBipartiteFourCycle1, MODE_A),
             partial(changeBipartiteFourCycle2, MODE_A)],
            ['bipartiteDensityA',
             'bipartiteActivityA',
             'bipartiteEgoTwoStarA',
             'bipartiteAlterTwoStar1A',
             'bipartiteAlterTwoStar2A',
             'bipartiteFourCycle1A',
             'bipartiteFourCycle2A'],
             '../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_outcome_BNA.txt',
            bipartite=True,
            sampler_func = partial(bipartiteALAAMsampler, MODE_A),
            run = runNumber
    )


if __name__ == "__main__":
    main()


