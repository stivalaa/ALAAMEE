#
# File:    zooALAAMSampler.py
# Author:  Alex Stivala
# Created: June 2020
#
"""ZOO (Zero-Or-One) ALAAM MCMC sampler. The ZOO sampler chooses between
   a node with 0 outcome or 1 outcome with probability 1/2 and then
   toggles the outcome on that node. I.e. it choose a zero-to-one or
   one-to-zero move with equal probability. The idea is that when the
   outcome (= 1) density is low, this should lead to better mixing
   than the "basic" ALAAM sampler, which by choosing a node uniformly
   at random will much more often propose a zero-to-one move when
   there is a small fraction of outcome=1 nodes in the observed data.

   This is the ALAAM analogue of the TNT (Tie-no-Tie) ERGM sampler.
   There is no citation for the ZOO sampler, but the Tie-no-tie (TNT)
   ERGM distribution sampler as described in:
 
      Morris, M., Handcock, M. S., & Hunter, D. R. (2008). Specification
      of exponential-family random graph models: terms and computational
      aspects. Journal of Statistical Software, 24(4), 1548.

"""

import random
import math
import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph,NA_VALUE
from changeStatisticsALAAM import *



def zooALAAMsampler(G, A, changestats_func_list, theta, performMove,
                      sampler_m):
    """
    zooALAAMsampler - sample from ALAAM distribution with Zero-Or-One (ZOO)
                      sampler, returning estimate of E(Delta_z(x_obs))

   The ZOO sampler chooses between
   a node with 0 outcome or 1 outcome with probability 1/2 and then
   toggles the outcome on that node. I.e. it choose a zero-to-one or
   one-to-zero move with equal probability.

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
        acceptance_rate      - sampler acceptance rate
        changeTo1ChangeStats - numpy vector of change stats for changeTo1 moves
        changeTo0ChangeStats - numpy vector of change stats for changeTo0 moves

    Note A is updated in place if performMove is True
    otherwise unchanged
    """
    n = len(changestats_func_list)

    # number of elements of A that are not NA (so 0 or 1)
    numNodes = len(A)
    num_not_na = len(A) - len(np.where(A == NA_VALUE)[0])

    accepted = 0
    changeTo1ChangeStats = np.zeros(n)
    changeTo0ChangeStats = np.zeros(n)
    for k in range(sampler_m):
        # ZOO sampler: first choose a zero-to-one or one-to-zero move
        # with equal probability (1/2) by choosing a node with 0
        # outcome or 1 outcome with equal probability, and then toggle
        # outcome variable for it.

        # if all non-NA elements are 1 then must do 1 to 0 move
        # of if all non-NA elements are 0 must do 0 to 1 move
        if len(np.where(A == 1)[0]) == num_not_na:
            isChangeToZero = True
        elif len(np.where(A == 0)[0]) == num_not_na:
            isChangeToZero = False
        else:
            isChangeToZero = (random.uniform(0, 1) < 0.5)

        i = np.random.choice(np.where(A == (1 if isChangeToZero else 0))[0])
        while A[i] == NA_VALUE:  # keep going until we get one that is not NA
            i = np.random.choice(np.where(A == (1 if isChangeToZero else 0))[0])
        
        if isChangeToZero:
            assert(A[i] == 1)
            A[i] = 0

        assert(A[i] == 0)

        # compute change statistics for each of the n statistics using the
        # list of change statistic functions
        changestats = np.zeros(n)
        for l in range(n):
            changestats[l] = changestats_func_list[l](G, A, i)
        changeSignMul = -1 if isChangeToZero else +1
        total = np.sum(theta * changeSignMul * changestats)

        Dmax = float(num_not_na)                # max possible outcome=1 nodes
        Dy   = float(len(np.where(A == 1)[0]))  # number of outcome=1 nodes now
        # TODO should handle special cases for all zero and all one
        if isChangeToZero:
            log_proposal_ratio = np.log(Dy / (Dmax - Dy))
        else:
            log_proposal_ratio = np.log((Dmax - Dy) / Dy)
        

        alpha = np.exp(log_proposal_ratio + total)#np.exp gives inf not overflow

        if random.uniform(0, 1) < alpha:
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

