#
# File:    equilibriumExpectation.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Python implementation of the Equilibrium Expectation algorithm
 for estimation of Autologistic Actor Attribute Model (ALAAM) parameters.

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

def algorithm_EE(G, A, changestats_func_list, theta, D0,
                 Mouter, M, theta_outfile, dzA_outfile,
                 sampler_func = basicALAAMsampler):
    """
    Algorithm EE

    Parameters:
       G                   - Graph object for graph to estimate
       A                   - vector of 0/1 outcome variables for ALAAM
       changestats_func_list-list of change statistics funcions
       theta               - corresponding vector of initial theta values
       D0                  - corresponding vector of inital D0 from Algorithm S
       Mouter              - iterations of Algorithm EE (outer loop)
       M                   - iterations of Algorithm EE (inner loop)
       theta_outfile       - open for write file to write theta values
       dzA_outfile         - open for write file to write dzA values
       sampler_func        - ALAAM sampler function with signature
                             (G, A, changestats_func_list, theta, performMove,
                              sampler_m); see basicALAAMsampler.py
                             default basicALAAMsampler

     Returns:
         numpy vector of theta values at end

    """
    ACA = 1e-09    # multiplier of D0 to get step size multiplier da (K_A)
    compC = 1e-02  # multiplier of sd(theta)/mean(theta) to limit theta variance
    n = len(changestats_func_list)
    dzA = np.zeros(n)  # zero outside loop, dzA accumulates in loop
    t = 0
    for touter in range(Mouter):
        thetamatrix = np.empty((M, n)) # rows theta vectors, 1 per inner iter
        for tinner in range(M):
            accepted = 0
            (acceptance_rate,
             changeTo1ChangeStats,
             changeTo0ChangeStats) = sampler_func(G, A,
                                                  changestats_func_list,
                                                  theta,
                                                  performMove = True,
                                                  sampler_m = sampler_m)
            dzA += changeTo1ChangeStats - changeTo0ChangeStats  # dzA accumulates here
            da = D0 * ACA
            theta_step = -np.sign(dzA) * da * dzA**2
            theta += theta_step
            thetamatrix[tinner,] = theta
            t += 1
        theta_outfile.write(str(t) + ' ' + ' '.join([str(x) for x in theta]) + 
                                ' ' + str(acceptance_rate) + '\n')
        dzA_outfile.write(str(t) + ' ' + ' '.join([str(x) for x in dzA]) + '\n')
        thetamean = np.mean(thetamatrix, axis = 0) # mean theta over inner loop
        thetasd   = np.std(thetamatrix, axis = 0)  # standard deviation
        thetamean = np.where(np.abs(thetamean) < 1, np.ones(n), thetamean) # enforce minimum magnitude 1 to stop sticking at zero
        DD = thetasd / np.abs(thetamean)
        D0 *= compC / DD # to limit size of fluctuations in theta (see S.I.)
        
    return theta


