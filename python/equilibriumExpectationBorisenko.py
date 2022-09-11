#
# File:    equilibriumExpectation.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Python implementation of the Equilibrium Expectation algorithm
 for estimation of Autologistic Actor Attribute Model (ALAAM) parameters.
 This is the simplified (Borisenko et al. 2019) version that has only the
 learning rate and not the other hyper-parameters.

 The EE algorithm is described in:

    Borisenko, A., Byshkin, M., & Lomi, A. (2019). A Simple Algorithm
    for Scalable Monte Carlo Inference. arXiv preprint
    arXiv:1901.00533. https://arxiv.org/abs/1901.00533

    Byshkin M, Stivala A, Mira A, Robins G, Lomi A (2018) "Fast
    maximum likelihood estimation via equilibrium expectation for
    large network data". Scientific Reports 8:11509
    doi:10.1038/s41598-018-29725-8


 The ALAAM is described in:

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.

"""

import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph
from changeStatisticsALAAM import *
from basicALAAMsampler import basicALAAMsampler

#
# Constants
#
THETA_PREFIX = 'theta_values_' # prefix for theta output filename
DZA_PREFIX = 'dzA_values_'     # prefix for dzA output filename
sampler_m  = 1000              # number of sampler iterations

def algorithm_EE(G, A, changestats_func_list, theta,
                 M, theta_outfile, dzA_outfile, learningRate = 0.01,
                 sampler_func = basicALAAMsampler):
    """
    Algorithm EE (Equilibrium Expectation).
    Version from Borisenko et al. (2019) with only learning rate
    and not the other original hyper-parameters.

    Parameters:
       G                   - Graph object for graph to estimate
       A                   - vector of 0/1 outcome variables for ALAAM
       changestats_func_list-list of change statistics funcions
       theta               - corresponding vector of initial theta values
       M                   - iterations of Algorithm EE (inner loop)
       theta_outfile       - open for write file to write theta values
       dzA_outfile         - open for write file to write dzA values
       learningRate        - learning rate (step size multiplier, a)
                             defult 0.01
       sampler_func        - ALAAM sampler function with signature
                             (G, A, changestats_func_list, theta, performMove,
                              sampler_m); see basicALAAMsampler.py
                             default basicALAAMsampler


     Returns:
         numpy vector of theta values at end

    """
    # Constants
    minTheta     = 0.01    # min abs value of theta to prevent zero update step

    n = len(changestats_func_list)

    # numpy vectpr versions of constants for convenience in using numpy
    learningRateVec = learningRate * np.ones(n)
    minThetaVec = minTheta * np.ones(n)

    dzA = np.zeros(n)  # zero outside loop, dzA accumulates in loop
    for t in range(M):
        accepted = 0
        (acceptance_rate,
         changeTo1ChangeStats,
         changeTo0ChangeStats) = sampler_func(G, A,
                                              changestats_func_list,
                                              theta,
                                              performMove = True,
                                              sampler_m = sampler_m)
        dzA += changeTo1ChangeStats - changeTo0ChangeStats  # dzA accumulates here
        theta_step = -np.sign(dzA) * learningRateVec * np.maximum(minThetaVec,
                                                                 np.abs(theta))

        theta += theta_step

        if t % 100 == 0:
            theta_outfile.write(str(t) + ' ' + ' '.join([str(x) for x in theta]) + 
                            ' ' + str(acceptance_rate) + '\n')
            dzA_outfile.write(str(t) + ' ' + ' '.join([str(x) for x in dzA]) + '\n')


    return theta


