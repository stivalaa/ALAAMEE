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
import sys

from Graph import Graph,NA_VALUE,int_or_na
from changeStatisticsALAAM import *
from simulateALAAM import simulateALAAM
from computeObservedStatistics import computeObservedStatistics
from basicALAAMsampler import basicALAAMsampler


def gof(G, Aobs, changestats_func_list, theta, numSamples = 1000,
        sampler_func = basicALAAMsampler, Ainitial = None,
        iterationInStep = 1000, burnIn = 10000,
        bipartiteFixedMode = None,
        outputStatsFilename = None,
        outputObsStatsFilename = None,
        labels = None
        ):
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
       numSamples           - number of simulations, default 1000
       sampler_func        - ALAAM sampler function with signature
                               (G, A, changestats_func_list, theta, performMove,
                                sampler_m); see basicALAAMsampler.py
                               default basicALAAMsampler
       Ainitial              - vector of 0/1 outcome variables to initialize
                               the outcome vector to before simulation process,
                               rather than starting from all 0 or random.
                               Default None, for random initialization.
       iterationInStep       - number of MCMC steps between each sample.
                               Default 1000.
       burnIn                - number of iterations to discard at start.
                               Default 10000.
       bipartiteFixedMode    - for bipartite networks only, the mode
                               (MODE_A or MODE_B that is fixed to NA
                               in simulation, for when outcome
                               variable not defined for that mode,
                               or None. Default None.
       outputStatsFilename   - Filename to write simulated statistics to or
                               None. Default None. WARNING: file overwritten.
       outputObsStatsFilename- Filename to write observed statistics to or
                               None. Default None. WARNING: file overwritten.
       labels                - list of strings corresponding to param_func_list
                               to label output (header line) in
                               simulated statistics writte to
                               outputStatsFilename.. Default None.
                               Must be set if outputStatsFilename or
                               outputObsStatsFilename is not None.

    Return value:
       tuple(tratios, mdist) where
          tratios is vector of t-ratios (one for each statistic)
          and mdist is Mahalanobis distance of observed statistics from
          statistics simualted from model
    """
    n = len(changestats_func_list)
    assert len(theta) == n
    assert not ((outputStatsFilename is not None or
                 outputObsStatsFilename is not None) and labels is None)

    print('Gof numSamples =', numSamples, 'iterationInStep =', iterationInStep, 'burnIn = ', burnIn)

    # Calculate observed statistics by summing change stats for each 1 variable
    Zobs = computeObservedStatistics(G, Aobs, changestats_func_list)

    # Write obseved statistics if output filename provided
    if outputObsStatsFilename is not None:
        with open(outputObsStatsFilename, 'w') as outfile:
            outfile.write(' '.join(labels) + '\n')
            outfile.write(' '.join([str(z) for z in Zobs]) + '\n')

    # Compute simulated outcome vector statistics from MCMC
    sim_results = simulateALAAM(G, changestats_func_list,  theta,
                                numSamples, iterationInStep, burnIn,
                                sampler_func, Ainitial,
                                bipartiteFixedMode, Aobs)

    # write simulated statistics if output filename provided
    if outputStatsFilename is not None:
        # sim_results is an iterator from simulateALAAM() so convert
        # to list since we need to use it again below in computing t-ratios etc
        # only include the parts we need (notably not simvec which might
        # use a lot of memory)
        # simulateALAAM() yields tuples (simvec,stats,acceptance_rate,t)
        sim_results = [(None, r[1], r[2], r[3]) for r in sim_results]
        with open(outputStatsFilename, 'w') as outfile:
            outfile.write(' '.join(['t'] + labels +
                                   ['acceptance_rate']) + '\n')
            for (simvec, stats, acceptance_rate, t) in sim_results:
                outfile.write(' '.join([str(t)] +
                                       [str(x) for x in list(stats)] +
                                       [str(acceptance_rate)]) + '\n')

    # simulateALAAM() return list of tuples (simvec,stats,acceptance_rate,t)
    # convert to matrix where each row is sample, each column is statistic
    Zmatrix = np.stack([r[1] for r in sim_results])
    assert(np.shape(Zmatrix) == (numSamples, n))
    Zmean = np.mean(Zmatrix, axis=0)
    Zsd = np.std(Zmatrix, axis=0)
    print('Zmatrix = ',Zmatrix) #XXX
    print('obs stats  =', Zobs)
    print('mean stats =', Zmean)
    print('sd stats   =', Zsd)
    
    # compute t-statistics
    tratio = (Zmean - Zobs) / Zsd

    # compute Mahalanobis distance
    mahaldist = mahalanobis(Zobs, Zmatrix)

    return (tratio,mahaldist)


def mahalanobis(u, X):
    """
    Mahalanobis distance of the observation vector u from the reference
    samples in X.

    Parameters:
       u  -  numpy vector of observation
       X  -  numpy array where each row is a sample (so columns are variables,
             the number of columns must equal the dimension of u)

    Retrurn value:
      Mahalanobis distance of u from distribution described by samples in X
    """
    colmeans = np.mean(X, axis=0) # axis=0 gives mean of each column
    # rowvar=False means each column is a variable, each row is an observation
    # in computing the covariance matrix
    Sigma = np.cov(X, rowvar = False)
    try:
        SigmaInv = np.linalg.inv(Sigma) # inverse covariance matrix
    except np.linalg.LinAlgError:
        warnmsg = "WARNING: covariance matrix is computationally singular, using pseudo-inverse of covariance matrix\n"
        sys.stderr.write(warnmsg)
        sys.stdout.write(warnmsg)
        SigmaInv = np.linalg.pinv(Sigma) # Moore-Penrose pseuo-inverse
    diffmean = u - colmeans
    Dsquared = np.dot(np.dot(diffmean, SigmaInv), diffmean) # diffmean^T*SimaInv*diffmean
    return math.sqrt(Dsquared)

