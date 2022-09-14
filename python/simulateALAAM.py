#
# File:    simualateALAAM.py
# Author:  Alex Stivala
# Created: May 2020
#
"""Python implementation of ALAAM simulation (generating binary outcome
   vectors given network, node attributes, ALAAM mode parmaters).

 The ALAAM is described in:

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.


 The example data is described in:

  Stivala, A. D., Gallagher, H. C., Rolls, D. A., Wang, P., & Robins,
  G. L. (2020). Using Sampled Network Data With The Autologistic Actor
  Attribute Model. arXiv preprint arXiv:2002.00849.

"""
import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph,NA_VALUE
from changeStatisticsALAAM import *
from basicALAAMsampler import basicALAAMsampler
from computeObservedStatistics import computeObservedStatistics



def rand_bin_array(K, N):
    """rand_bin_array - binary vector of length N with exactly K ones
                        at random indices

    Parameters:
        K  - number of ones
        N  - length of vector

    Return value:
       numpy array of length N with K ones at random positions (others 0)

    https://stackoverflow.com/questions/19597473/binary-random-array-with-a-specific-proportion-of-ones
    """
    arr = np.zeros(N)
    arr[:K]  = 1
    np.random.shuffle(arr)
    return arr



def simulateALAAM(G, changestats_func_list, theta, numSamples,
                  iterationInStep = None, burnIn = None,
                  sampler_func = basicALAAMsampler, Ainitial = None):
    """
    Simulate ALAAM (generate binary outcome vector) given model parameters
    and network (including node attributes).
    This is a generator function (i.e. use it as an iterator).


    Parameters:
       G                   - Graph object for graph to simulate ALAAM on
       changestats_func_list-list of change statistics funcions
       theta               - corresponding vector of theta values
       numSamples          - number of samples to yield
       iterationInStep     - number of sampler iterations 
                             i.e. the number of iterations between samples
                             (or 10*numNodes if None)
       burnIn              - number of samples to discard at start
                             (or 10*iterationInStep if None)
       sampler_func        - ALAAM sampler function with signature
                             (G, A, changestats_func_list, theta, performMove,
                              sampler_m); see basicALAAMsampler.py
                             default basicALAAMsampler
       Ainitial              - vector of 0/1 outcome variables to initialize
                               the outcome vector to before simulation process,
                               rather than starting from all 0 or random.
                               Default None, for random initialization here.


     Returns:
       This is a generator function that yields tuple
        (A, stats, acceptance_Rate, t) where
          A is vector of 0/1 ALAAM outcome and
          stats is vector of the model sufficient statistics
          acceptance_rate is the sampler acceptance rate
          t is the iteration number
       values on each call.
    """
    assert len(theta) == len(changestats_func_list)

    if iterationInStep is None:
        iterationInStep = 10 * G.numNodes()

    if burnIn is None:
        burnIn = 10*iterationInStep

    if Ainitial is not None:
        A = np.copy(Ainitial)
    else:
        START_FROM_ZERO = False 
        if START_FROM_ZERO: # start from zero vector
            A = np.zeros(G.numNodes())  # initialize outcmoe vector to zero
        else:   # do not use all zero,to avoid special case of proposal probability
            # initialize outcome vector to 50% ones
            A = rand_bin_array(int(0.5*G.numNodes()), G.numNodes())


            # TODO: for bipartite graphs, should do the following,
            # but allow either A or B mode to be all NA (which means
            # the sampler never changes that value):
            ## For bipartite graph, make sure initial outcome vector 
            ## is all NA for the B mode (assuming we are using 
            ## outcome only on A mode here) and 0 or 1 with 
            ## uniform probability for A mode
            # A = np.concatenate(
            #            (rand_bin_array(int(0.5*G.num_A_nodes), G.num_A_nodes),
            #             np.ones(G.num_B_nodes)*NA_VALUE) )

    # And compute observed statistics by summing change stats for each
    # 1 variable (note if instead starting at all zero A vector don't
    # have to do this as then Z is zero vector)

    Z = computeObservedStatistics(G, A, changestats_func_list)

    (acceptance_rate,
     changeTo1ChangeStats,
     changeTo0ChangeStats) = sampler_func(G, A,
                                          changestats_func_list,
                                          theta,
                                          performMove = True,
                                          sampler_m = burnIn)
    Z += changeTo1ChangeStats - changeTo0ChangeStats

    for i in range(numSamples):
        (acceptance_rate,
         changeTo1ChangeStats,
         changeTo0ChangeStats) = sampler_func(G, A,
                                              changestats_func_list,
                                              theta,
                                              performMove = True,
                                              sampler_m = iterationInStep)
        Z += changeTo1ChangeStats - changeTo0ChangeStats
        yield (np.array(A), np.array(Z), acceptance_rate, (i+1)*iterationInStep+burnIn)
