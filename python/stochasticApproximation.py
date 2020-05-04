#
# File:    stochasticApproximation.py
# Author:  Alex Stivala
# Created: May 2020
#
"""Simple demonstration implementation of the Robbins-Monro stochastic
 approximatino algorithm for estimation of Autologistic Actor
 Attribute Model (ALAAM) parameters. 

 The Robbins-Monro algorithm for ERGM (rather than ALAAM) is described in:

  Snijders, T. A. (2002). Markov chain Monte Carlo estimation of
  exponential random graph models. Journal of Social Structure, 3(2),
  1-40.

 The ALAAM is described in:

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.

"""
import sys
import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph
from changeStatisticsALAAM import *
from basicALAAMsampler import basicALAAMsampler

#
# Constants
#
sampler_m  = 1000              # number of sampler iterations

def stochasticApproximation(G, A, changestats_func_list, theta):
    """
    Robbins-Monro stochastic approximation to estimate ALAAM parameers.

    The Robbins-Monro algorithm for ERGM (rather than ALAAM) is described in:

     Snijders, T. A. (2002). Markov chain Monte Carlo estimation of
     exponential random graph models. Journal of Social Structure, 3(2),
     1-40.

    Parameters:
       G                   - Graph object for graph to estimate
       A                   - vector of 0/1 outcome variables for ALAAM
       changestats_func_list-list of change statistics funcions
       theta               - corresponding vector of initial theta values

     Returns:
         numpy vector of theta values at end (or None if degenerate model)

    """
    #epsilon = np.finfo(float).eps
    epsilon = 1e-08
    
    n = len(changestats_func_list)

    # phase 1 constants
    phase1steps     = 7 + 3*n
    iterationInStep = 10 * G.numNodes()

    # phase 2 constants
    
    
    # phase 3 constants

    
    #
    # Phase 1: estimate covariance matrix
    #
    Zmatrix = np.empty((phase1steps, n)) # rows statistics Z vectors, 1 per step
    for i in xrange(phase1steps):
        accepted = 0
        (acceptance_rate,
         changeTo1ChangeStats,
         changeTo0ChangeStats) = basicALAAMsampler(G, A,
                                                   changestats_func_list,
                                                   theta,
                                                   performMove = True,
                                                   sampler_m = iterationInStep)
        Z = changeTo1ChangeStats - changeTo0ChangeStats
        Zmatrix[i, ] = Z
    D = (1.0/iterationInStep) * np.cov(np.transpose(Zmatrix))
    if 1.0/np.linalg.cond(D) < epsilon:
        sys.stdout.write("Covariance matrix is singular: degenerate model\n")
        return None
    D0 = np.diag(D)
    Dinv = np.linalg.inv(D)
    
    print D #XXX
    print D0 #XXX
    
    #
    # Phase 2 (main phase): In each subphase, generate simulated
    # networks according to current parameter (theta) value, and
    # update theta according to Robbins-Monro formula between
    # subphases. Terminate when sum within subphase of successive
    # products of statistics is non-negative (or iteration limit).
    # At end of each subphase average theta over subphase is used as
    # new theta value. Value of Robbins-Monro multiplier a is halved
    # between each subphase.
    #


    #
    # Phase 3: Used only to estimate covariance matrix of estimator and
    # check for approximate validity of solution of moment equation.
    # 

    return theta


