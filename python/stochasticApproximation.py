#
# File:    stochasticApproximation.py
# Author:  Alex Stivala
# Created: May 2020
#
"""Python implementation of the Robbins-Monro stochastic
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
import sys, time
import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph,NA_VALUE
from changeStatisticsALAAM import *
from basicALAAMsampler import basicALAAMsampler


def stochasticApproximation(G, Aobs, changestats_func_list, theta0,
                            Zobs, sampler_func=basicALAAMsampler):
    """
    Robbins-Monro stochastic approximation to estimate ALAAM parameers.

    The Robbins-Monro algorithm for ERGM (rather than ALAAM) is described in:

     Snijders, T. A. (2002). Markov chain Monte Carlo estimation of
     exponential random graph models. Journal of Social Structure, 3(2),
     1-40.

    Parameters:
       G                   - Graph object for graph to estimate
       Aobs                - vector of 0/1 outcome variables for ALAAM
       changestats_func_list-list of change statistics funcions
       theta0              - corresponding vector of initial theta values
       Zobs                - vector of observed statistics
                             (from computeObservedStatistics)
       sampler_func        - ALAAM sampler function with signature
                             (G, A, changestats_func_list, theta, performMove,
                              sampler_m); see basicALAAMsampler.py
                             default basicALAAMsampler


     Returns:
         tuple (theta, std_error, t_ratio) of numpy vectors for
         parameter values, standard error estimates, t-ratios, respectively,
         or None if degenerate model

    """
    epsilon = np.finfo(float).eps
    
    n = len(changestats_func_list)

    # copy input parameter vectors so input vectors not modified
    A     = np.copy(Aobs)
    theta = np.copy(theta0)
    
    # constants used in multiple phases
    iterationInStep = 10 * G.numNodes()
    #XXX testing:iterationInStep = 50#XXX
    
    # phase 1 constants
    phase1steps     = 7 + 3*n

    # phase 2 constants
    numSubphases  = 5
    a_initial     = 0.01  # initial value of Robbins-Monro step size

    # phase 3 constants
    phase3steps = 1000
    burnin       = int(round(0.1 * phase3steps * iterationInStep))
    
    #
    # Phase 1: estimate covariance matrix
    #
    print('Phase 1 steps = ', phase1steps, 'iters per step = ',iterationInStep)
    start = time.time()
    Z = np.copy(Zobs)  # start at observed statistics vector
    Zmatrix = np.empty((phase1steps, n)) # rows statistics Z vectors, 1 per step
    for i in range(phase1steps):
        (acceptance_rate,
         changeTo1ChangeStats,
         changeTo0ChangeStats) = sampler_func(G, A,
                                              changestats_func_list,
                                              theta,
                                              performMove = True,
                                              sampler_m = iterationInStep)
        Z += changeTo1ChangeStats - changeTo0ChangeStats
        Zmatrix[i, ] = Z

    Zmean = np.mean(Zmatrix, axis=0)
    Zmean = np.reshape(Zmean, (1, len(Zmean))) # make it a row vector
    theta = np.reshape(theta, (1, len(theta)))
    print('Zmean = ', Zmean)

    # Dcov = np.cov(np.transpose(Zmatrix))
    # print 'Dcov = ', Dcov

    Zmatrix -= Zmean
    D = (1.0/phase1steps) * np.matmul(np.transpose(Zmatrix), Zmatrix)

    print('D = ')
    print(D)

    if 1.0/np.linalg.cond(D) < epsilon:
        sys.stdout.write("Covariance matrix is singular: may be degenerate model\n")
        return (None, None, None)
    Dinv = np.linalg.inv(D)


    print('Phase 1 took', time.time() - start, 's')

    #
    # Phase 2 (main phase): In each subphase, generate simulated
    # networks according to current parameter (theta) value, and
    # update theta according to Robbins-Monro formula.
    # Terminate when sum within subphase of successive
    # products of statistics is non-negative (or iteration limit).
    # At end of each subphase average theta over subphase is used as
    # new theta value. Value of Robbins-Monro multiplier a is halved
    # between each subphase.
    #
    print('Phase 2 subphases = ',numSubphases, ' iters per step = ', iterationInStep)
    start = time.time()
    a = a_initial
    for k in range(numSubphases):
        NkMin  = int(round(2.0**(4.0 * k / 3.0) * (7 + n)))
        NkMax  = NkMin + 200
        print('subphase', k, 'a = ', a, 'NkMin = ',NkMin,'NkMax = ',NkMax, 'theta = ', theta)
        i = 0
        sumSuccessiveProducts = np.zeros(n)
        thetaSum = np.zeros((1,n))
        while i < NkMax and (i <= NkMin or not np.all(sumSuccessiveProducts < 0)):
            oldZ = np.copy(Z)
            (acceptance_rate,
             changeTo1ChangeStats,
             changeTo0ChangeStats) = sampler_func(G, A,
                                                  changestats_func_list,
                                                  theta,
                                                  performMove = True,
                                                  sampler_m = iterationInStep)
            Z += changeTo1ChangeStats - changeTo0ChangeStats

            theta_step = a * np.matmul(Dinv, Z - Zobs)
            theta -= theta_step
            thetaSum += theta
            sumSuccessiveProducts += ((Z - Zobs) * (oldZ - Zobs))
            ##print '    sumSuccessiveProducts =',sumSuccessiveProducts
            i += 1
        if k > 1:     # use initial value of a in first two subphases
            a /= 2.0  # otherwise halve a for next subphase (gain sequence)
        print('  subphase',k,'finished after',i,'iterations (acceptance rate =',acceptance_rate,')')
        theta = thetaSum / i # average theta

    print('Phase 2 took', time.time() - start, 's')
    
    #
    # Phase 3: Used only to estimate covariance matrix of estimator and
    # check for approximate validity of solution of moment equation.
    # 
    print('Phase 3 steps = ', phase3steps, 'iters per step = ',iterationInStep, 'burnin = ', burnin)
    start = time.time()
    Zmatrix = np.empty((phase3steps, n)) # rows statistics Z vectors, 1 per step

    # burn-in iterations
    (acceptance_rate,
     changeTo1ChangeStats,
     changeTo0ChangeStats) = sampler_func(G, A,
                                          changestats_func_list,
                                          theta,
                                          performMove = True,
                                          sampler_m = burnin)
    Z += changeTo1ChangeStats - changeTo0ChangeStats

    
    for i in range(phase3steps):
        (acceptance_rate,
         changeTo1ChangeStats,
         changeTo0ChangeStats) = sampler_func(G, A,
                                              changestats_func_list,
                                              theta,
                                              performMove = True,
                                              sampler_m = iterationInStep)
        Z += changeTo1ChangeStats - changeTo0ChangeStats
        Zmatrix[i, ] = Z

    print('XXX Zmatrix = ')
    print(Zmatrix) #XXX

    Zmean = np.mean(Zmatrix, axis=0)
    Zmean = np.reshape(Zmean, (1, len(Zmean))) # make it a row vector
    print('Phase 3 Zmean = ', Zmean)

    # Dcov = np.cov(np.transpose(Zmatrix))
    # print 'Dcov = ', Dcov

    Zmatrix -= Zmean
    D = (1.0/phase3steps) * np.matmul(np.transpose(Zmatrix), Zmatrix)

    print('Phase 3 covariance matrix D = ')
    print(D)
    
    if 1.0/np.linalg.cond(D) < epsilon:
        sys.stdout.write("Phase 3 covariance matrix is singular: may be degenerate model\n")
        return (None, None, None)

    D0 = np.copy(np.diag(D))
    Dinv = np.linalg.inv(D)
    D0inv = 1.0/D0

    std_error = np.sqrt(np.diag(Dinv))
    t_ratio = (Zmean - Zobs) * np.sqrt(D0inv)


    print('Phase 3 took', time.time() - start, 's')
    theta = np.reshape(theta, (n ,))     # plain np array again
    t_ratio = np.reshape(t_ratio, (n ,))
    return (theta, std_error, t_ratio)


