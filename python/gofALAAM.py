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
        iterationInStep = 1000, burnIn = 10000):
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

    Return value:
       tuple(tratios, mdist) where
          tratios is vector of t-ratios (one for each statistic)
          and mdist is Mahalanobis distance of observed statistics from
          statistics simualted from model
    """
    n = len(changestats_func_list)
    assert len(theta) == n

    print('Gof numSamples =', numSamples, 'iterationInStep =', iterationInStep, 'burnIn = ', burnIn)

    # Calculate observed statistics by summing change stats for each 1 variable
    Zobs = computeObservedStatistics(G, Aobs, changestats_func_list)

    # Compute simulated outcome vector statistics from MCMC
    sim_results = simulateALAAM(G, changestats_func_list,  theta,
                                numSamples, iterationInStep, burnIn,
                                sampler_func, Ainitial, Aobs = Aobs)
    #simulateALAAM() return list of tuples (simvec,stats,acceptance_rate,t)
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

