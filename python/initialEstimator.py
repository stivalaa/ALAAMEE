#
# File:    initialEstimator.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Intiial parameter estimates 
 for estimation of Autologistic Actor Attribute Model (ALAAM) parameters
 using a form of contrastive divergence:

 The EE algorithm is described in:

    Borisenko, A., Byshkin, M., & Lomi, A. (2019). A Simple Algorithm
    for Scalable Monte Carlo Inference. arXiv preprint
    arXiv:1901.00533. https://arxiv.org/abs/1901.00533

    Byshkin M, Stivala A, Mira A, Robins G, Lomi A (2018). "Fast
    maximum likelihood estimation via equilibrium expectation for
    large network data". Scientific Reports 8:11509
    doi:10.1038/s41598-018-29725-8

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



def algorithm_S(G, A, changestats_func_list, M1, theta_outfile,
                sampler_func = basicALAAMsampler):
    """

     Algorithm S

     Parameters:
        G                   - Graph object for graph to estimate
        A                   - vector of 0/1 outcome variables for ALAAM
        changestat_func_v   - vector of change statistics funcions
        M1                  - number of iterations of Algorithm S
        theta_outfile       - open for write file to write theta values
        sampler_func        - ALAAM sampler function with signature
                             (G, A, changestats_func_list, theta, performMove,
                              sampler_m); see basicALAAMsampler.py
                             default basicALAAMsampler


     Returns:
       tuple with:
         theta               - numpy vector of theta values at end
         Dmean               - derivative estimate value at end

    """
    ACA = 0.1 # multiplier of da to get K1A step size multiplier
    n = len(changestats_func_list)
    theta = np.zeros(n)
    D0 = np.zeros(n)
    for t in range(M1):
        accepted = 0
        (acceptance_rate,
         changeTo1ChangeStats,
         changeTo0ChangeStats) = sampler_func(G, A,
                                              changestats_func_list,
                                              theta,
                                              performMove = False,
                                              sampler_m = sampler_m)
        dzA = changeTo0ChangeStats - changeTo1ChangeStats
        dzAmean = dzA / sampler_m
        sumChangeStats = changeTo1ChangeStats + changeTo0ChangeStats
        D0 += dzA**2 # 1/D0 is squared derivative
        da = np.zeros(n)
        for l in range(n):
            if (sumChangeStats[l] != 0):
                da[l] = ACA  / sumChangeStats[l]**2
        theta_step = np.sign(dzAmean) * da * dzA**2
        MAXSTEP = 0.1 # limit maximum step size
        theta_step = np.where(theta_step > MAXSTEP, MAXSTEP, theta_step)
        theta += theta_step
        theta_outfile.write(str(t-M1) + ' ' + ' '.join([str(x) for x in theta])
                            + ' ' + str(acceptance_rate) + '\n')
    Dmean = sampler_m / D0
    return(theta, Dmean)
        
