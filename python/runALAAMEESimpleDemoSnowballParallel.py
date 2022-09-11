#!/usr/bin/env python3
#
# File:    runALAAMEESimpleDemoSnowballParallel.py
# Author:  Alex Stivala
# Created: March 2021
#
"""Run the python implementation of the Equilibrium 
 Expecttation (EE) algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters, on snowball sampled network data.

 This version takes run number parameter so that
 parallel runs can be run with GNU parallel or PBS or Slurm job arrays.

 Usage:
     runALAAMEESimpleDemoSnowballParallel.py num_waves num_seeds runNumber


 The num_waves and num_seeds are only used to build the filenames of
 the snowball sampled network and attributes and zones files created
 by snowballSampleFromExampleData.R script with the same parameters run from
 the run_conditional_ee_example_parallel.sh script in examples/conditional/.


  E.g. for 16 parallel runs with GNU Parallel:

  seq 0 15 |  parallel -j 16 --progress --joblog parallel.log runALAAMEESimpleDemoSnowballParallel.py 3 10


 Citation for GNU parallel:

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

from conditionalALAAMsampler import conditionalALAAMsampler
from changeStatisticsALAAM import *
import  estimateALAAMEE


def usage(progname):
    """
    print usage msg and exit
    """
    sys.stderr.write("usage: " + progname + " num_waves num_seeds\n")
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

    if len(args) != 3:
        usage(sys.argv[0])

    waves = int(args[0])
    seeds = int(args[1])
    runNumber = int(args[2])

    print('Conditional estimation on snowball sample with ' + str(waves) + ' waves and ' + str(seeds) + ' seeds')

    sampled_filenames_part = "_waves" + str(waves) + "_seeds" + str(seeds)

    estimateALAAMEE.run_on_network_attr(
        'n500_kstar_simulate12750000' + sampled_filenames_part + '_num6700000.txt',
        [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
        ["Density", "Activity", "Contagion", "Binary", "Continuous"],
        'sample-n500_bin_cont6700000' + sampled_filenames_part + '.txt',
        'binaryAttribute_50_50_n500' + sampled_filenames_part + '_num6700000.txt',
        'continuousAttributes_n500' + sampled_filenames_part  + '_num6700000.txt',
        catattr_filename = None,
        run = runNumber,
        sampler_func = conditionalALAAMsampler,
        zone_filename = 'snowball_zonefile' + sampled_filenames_part + '_num6700000.txt')




if __name__ == "__main__":
    main()


