#
# File:    conditionalALAAMSampler.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""basic ALAAM MCMC sampler, for estimation conditional on snowball
   sampling structure. A node from one of the inner waves (i.e. any
   other that the outermost snowball sampling zone) is chosen
   uniformly at random and its outcome binary variable value toggled.

  The ALAAM is described in:

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.


 The example data and conditional estimation for snowball sampling
 is described in:

  Stivala, A. D., Gallagher, H. C., Rolls, D. A., Wang, P., & Robins,
  G. L. (2020). Using Sampled Network Data With The Autologistic Actor
  Attribute Model. arXiv preprint arXiv:2002.00849.

"""

import random
import math
import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph,NA_VALUE
from changeStatisticsALAAM import *



def conditionalALAAMsampler(G, A, changestats_func_list, theta, performMove,
                      sampler_m):
    """
    conditionalALAAMsampler - sample from ALAAM distribution with basic sampler,
                   conditional on snowball sampling structure.

    In ALAAM there is a fixed network and a vector of binary outcome
    variables (indexed 0..N-1 corresponding to network nodes). Only
    the outcome vector is changed in MCMC simulations, the network is
    fixed.

    Parameters:
       G                   - Graph object for network (fixed)
       A                   - vector of 0/1 outcome variables for ALAAM
       changestats_func_list  - list of change statistics funcions
       theta               - numpy vector of theta (parameter) values
       performMove         - if True, actually do the MC move,
                             updating the outcome vector A
                             (otherwise are not modified)
       sampler_m           - number of proposals (iterations of sampler)

    Returns:
        acceptance_rate     - sampler acceptance rate
        changeTo1ChangeStats      - numpy vector of change stats for changeTo1 moves
        changeTo0ChangeStats      - numpy vector of change stats for changeTo0  moves

    Note A is updated in place if performMove is True
    otherwise unchanged
    """
    n = len(changestats_func_list)
#    assert(len(theta) == n)
    accepted = 0
    changeTo1ChangeStats = np.zeros(n)
    changeTo0ChangeStats = np.zeros(n)
    for k in range(sampler_m):
        # basic sampler, conditional on snowball sampling zone: select
        # a node in the inner waves (i.e. in any but the outermost
        # wave) uniformly at random and toggle outcome variable for it
        i = random.sample(G.inner_nodes, 1)[0]
        while A[i] == NA_VALUE:  # keep going until we get one that is not NA
            i = random.sample(G.inner_nodes, 1)[0]
        isChangeToZero = (A[i] == 1)
        if isChangeToZero:
            A[i] = 0

        # compute change statistics for each of the n statistics using the
        # list of change statistic functions
        changestats = np.zeros(n)
        for l in range(n):
            changestats[l] = changestats_func_list[l](G, A, i)
        changeSignMul = -1 if isChangeToZero else +1
        total = np.sum(theta * changeSignMul * changestats)
        if random.uniform(0, 1) < np.exp(total): #np.exp gives inf not overflow
            accepted += 1
            if performMove:
                # actually accept the move.
                # if changing to 0, we have already done it.
                # For changeTo1 move, set outcome to 1 now
                if not isChangeToZero:
                    A[i] = 1
            else:
                # if we are not to actually perform the moves, then reverse
                # changes for changeTo0 move made so A same as before
                if isChangeToZero:
                    A[i] = 1
            if isChangeToZero:
                changeTo0ChangeStats += changestats
            else:
                changeTo1ChangeStats += changestats
        elif isChangeToZero: # move not accepted, so reverse change 
            A[i] = 1

    acceptance_rate = float(accepted) / sampler_m
    return (acceptance_rate, changeTo1ChangeStats, changeTo0ChangeStats)

