#
# File:    bipartiteALAAMSampler.py
# Author:  Alex Stivala
# Created: September 2022
#
"""basic ALAAM MCMC sampler for bipartite (two-mode) networks.  A node
   is chosen uniformly at random and its outcome binary variable value
   toggled.

  The ALAAM is described in:

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.

"""

import random
import math
from functools import partial
import numpy as np         # used for matrix & vector data types and functions

from utils import NA_VALUE
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B


def bipartiteALAAMsampler(mode,
                          G, A, changestats_func_list, theta, performMove,
                          sampler_m):
    """
    bipartiteALAAMsampler - sample from ALAAM distribution on bipartite
                            network with basic sampler,
                           returning estimate of E(Delta_z(x_obs))

    In ALAAM there is a fixed network and a vector of binary outcome
    variables (indexed 0..N-1 corresponding to network nodes). Only
    the outcome vector is changed in MCMC simulations, the network is
    fixed.

    This version for bipartite networks takes as its first parameter
    the network mode (MODE_A or MODE_B) for which the outcome variable
    is defined (usually it is only defined for one mode). Only
    the outcome variable for nodes in this mode is varied in the MCMC process,
    the others are fixed. Note that this can also be done with
    basicALAAMsampler() just by setting all values in the other mode
    to NA, but this is more efficient.

    The mode for which outcome variable is defined (and therefore varied
    in MCMC) is the first parameter, to allow use of functools.partial()
    to make it a function with the signature (parameters)

    (G, A, changestats_func_list, theta, performMove, sampler_m)

    
    required by estaimteALAAMSA.run_on_network_attr() and
    simulateALAAM(), etc. it.e those functions that take a sampler
    function as a parameter. So instead of passing basicSampler
    as the sampler_func argument, instead pass

    partial(bipartiteSampler, MODE_A) or partial(bipartiteSampler, MODE_B)

    as required, just as is done for the change statistics functions
    in changeStatisticsALAAMbipartite.py.
    
    Parameters:
       mode                - network mode (node type) MODE_A or MODE_B
                             on which the outcome variables in A are defined.
       G                   - BipartiteGraph object for network (fixed)
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
    assert mode in [MODE_A, MODE_B]
    n = len(changestats_func_list)
    accepted = 0
    changeTo1ChangeStats = np.zeros(n)
    changeTo0ChangeStats = np.zeros(n)
    for k in range(sampler_m):
        # basic sampler for two-mode network: select a node i of the
        # specified mode unfiormly at random and toggle outcome
        # variable for it
        i = G.random_node(mode)
        while A[i] == NA_VALUE:  # keep going until we get one that is not NA
            i = G.random_node(mode)
        assert G.bipartite_node_mode(i) == mode
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

