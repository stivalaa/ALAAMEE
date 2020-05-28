#
# File:    gofALAAM.py
# Author:  Alex Stivala
# Created: May 2020
#
"""ALAAM goodness-of-fit by simulating from estimated parameters, and 
   comparing observed statistics to statistics of simulated outcome vectors,
   including statistics not included in the estimated model.

 The ALAAM is described in:

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.
"""
import math
import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph,NA_VALUE,int_or_na
from changeStatisticsALAAM import *
from simulateALAAM import simulateALAAM
from computeObservedStatistics import computeObservedStatistics


def gof(G, Aobs, changestats_func_list, theta, numSamples = 100):
    """
    ALAAM goodness-of-fit by simulating from estimated parameters, and 
    comparing observed statistics to statistics of simulated outcome vectors,
    including statistics not included in the estimated model.

    Parameters:
       G                    - Graph object of observed network
       Aobs                 - vector of 0/1 observed outcome variables for ALAAM
       changestats_func_list-list of change statistics functions
       theta                - corresponding vector of estimated theta values
                              (0 for those not included in estiamted model)
       numSamples           - number of simulations, default 100

    Return value:
       vector of t-ratios
    """
    n = len(changestats_func_list)
    assert len(theta) == n

    # Calculate observed statistics by summing change stats for each 1 variable
    Zobs = computeObservedStatistics(G, Aobs, changestats_func_list)

    # Compute simulated outcome vector statistics from MCMC
    sim_results = simulateALAAM(G, changestats_func_list,  theta,
                                numSamples = 100)
    #simulateALAAM() return list of tuples (simvec,stats,acceptance_rate,t)
    # convert to matrix where each row is sample, each column is statistic
    Zmatrix = np.stack([r[1] for r in sim_results])
    assert(np.shape(Zmatrix) == (numSamples, n))
    Zmean = np.mean(Zmatrix, axis=0)
    Zsd = np.std(Zmatrix, axis=0)
    print Zmatrix #XXX
    print 'obs stats  =', Zobs
    print 'mean stats =', Zmean
    print 'sd stats   =', Zsd
    
    # compute t-statistics
    tratio = (Zmean - Zobs) / Zsd

    return tratio

