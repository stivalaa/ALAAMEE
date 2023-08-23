#!/usr/bin/env python3
#
# File:    run runALAAMsimulatePokec.py
# Author:  Alex Stivala
# Created: July 2023
#
"""Simulate from  Autologistic Actor Attribute Model (ALAAM).

   Usage: runALAAMsimulatePokec.py TASK_ID

   where TASK_ID is supplied by SLURM_ARRAY_TASK_ID in the range
   0..200 and we here do (TASK_ID - 100)/100 to get in interval [-1.0, 1.0] 
"""
import sys
from functools import partial
import numpy as np
from math import log

from changeStatisticsALAAM import *
from basicALAAMsampler import basicALAAMsampler
from simulateALAAM import simulateALAAM


def simulate_from_network_attr(arclist_filename, param_func_list, labels,
                               theta,
                               binattr_filename=None,
                               contattr_filename=None,
                               catattr_filename=None,
                               sampler_func = basicALAAMsampler,
                               numSamples = 100,
                               iterationInStep = None,
                               burnIn = None):
    """Simulate ALAAM from on specified network with binary and/or continuous
    and categorical attributes.
    
    Parameters:
         arclist_filename - filename of Pajek format arclist 
         param_func_list   - list of change statistic functions corresponding
                             to parameters to estimate
         labels            - list of strings corresponding to param_func_list
                             to label output (header line)
         theta             - correponding vector of theta values
         binattr_filename - filename of binary attributes (node per line)
                            Default None, in which case no binary attr.
         contattr_filename - filename of continuous attributes (node per line)
                            Default None, in which case no continuous attr.
         catattr_filename - filename of categorical attributes (node per line)
                            Default None, in which case no categorical attr.
         sampler_func        - ALAAM sampler function with signature
                               (G, A, changestats_func_list, theta, performMove,
                                sampler_m); see basicALAAMsampler.py
                               default basicALAAMsampler
         iterationInStep  - number of sampler iterations
                             i.e. the number of iterations between samples
                             (or 10*numNodes if None)
         numSamples       - Number of samples (default 100)
         burnIn           - Number of sampels to discard at start
                            (or 10*iterationInStep if None)


    """
    assert(len(param_func_list) == len(labels))


    G = Graph(arclist_filename, binattr_filename, contattr_filename,
              catattr_filename)

    #G.printSummary()

    degseq = np.array([G.degree(v) for v in G.nodeIterator()])

    sys.stdout.write(' '.join(['t'] + [('theta_' + z) for z in labels] + labels + ['acceptance_rate', 'meanDegree1', 'varDegree1', 'meanDegree0', 'varDegree0']) + '\n')
    for (simvec,stats,acceptance_rate,t) in simulateALAAM(G, param_func_list,
                                                          theta,
                                                          numSamples,
                                                          iterationInStep,
                                                          burnIn,
                                                          sampler_func = sampler_func):
        ## mean and variance of degrees of nodes with outcome = 1
        meanDegree1 = np.mean(degseq[np.nonzero(simvec)[0]])
        varDegree1 = np.var(degseq[np.nonzero(simvec)[0]])
        ## mean and variance of degrees of nodes with outcome = 0
        meanDegree0 = np.mean(degseq[np.nonzero(simvec == 0)[0]])
        varDegree0 = np.var(degseq[np.nonzero(simvec == 0)[0]])

        sys.stdout.write(' '.join([str(t)] +
                                  [str(th) for th in list(theta)] +
                                  [str(x) for x in list(stats)] +
                                  [str(acceptance_rate)] +
                                  [str(x) for x in [meanDegree1, varDegree1,
                                                    meanDegree0, varDegree0]]) +
                                  '\n')



    
def usage(progname):
    """
    print usage msg and exit
    """
    sys.stderr.write("usage: " + progname + " TASK_ID\n")
    sys.exit(1)

###
### main
###


if len(sys.argv) != 2:
    usage(sys.argv[0])

TASK_ID = int(sys.argv[1])

theta_gwactivity = (TASK_ID - 100) / 100    

# parameters and corresponding labels 
param_func_list =      [changeDensity, partial(changeGWActivity, log(2.0)), changeActivity, changeContagion]
labels =               ["Density",     "GWActivity",                        "Activity",     "Contagion"]

theta =       np.array([-0.155,        theta_gwactivity,                    0,              -0.008])

assert len(param_func_list) == len(labels)
assert len(theta) == len(param_func_list)



simulate_from_network_attr(
    '../../../pokec/data/soc-pokec-relationships-undirected.net',
    param_func_list,
    labels, 
    theta,
    sampler_func = basicALAAMsampler,
    iterationInStep = 1000000,
    burnIn = 10000000
    )



