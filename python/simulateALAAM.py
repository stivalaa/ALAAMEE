#
# File:    simualateALAAM.py
# Author:  Alex Stivala
# Created: May 2020
#
"""Simple demonstration of ALAAM simulation (generating binary outcome
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


def simulateALAAM(G, changestats_func_list, theta, numSamples,
                  iterationInStep = None):
    """
    Simulate ALAAM (generate binary outcome vector) given model parameters
    and network (including node attributes).
    This is a generator function (i.e. use it as an iterator).


    Parameters:
       G                   - Graph object for graph to simlulate ALAAM on
       changestats_func_list-list of change statistics funcions
       theta               - corresponding vector of theta values
       numSamples          - number of samples to yield
       iterationInStep     - number of sampler iterations 
                             i.e. the number of iterations between samples
                             (or 10*numNodes if None)

     Returns:
       This is a generator function that yields vector of 0/1 ALAAM outcome
       values on each call.
    """
    assert len(theta) == len(changestats_func_list)

    if iterationInStep is None:
        iterationInStep = 10 * G.numNodes()

    A = np.zeros(G.numNodes())  # initial outcome vector
    dzA = np.zeros(len(theta))  # accumulated change statistics

    for i in xrange(numSamples):
        (acceptance_rate,
         changeTo1ChangeStats,
         changeTo0ChangeStats) = basicALAAMsampler(G, A,
                                                   changestats_func_list,
                                                   theta,
                                                   performMove = True,
                                                   sampler_m = iterationInStep)
        dzA += changeTo1ChangeStats - changeTo0ChangeStats
        yield A
