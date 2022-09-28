#
# File:    estimateALAAMSA.py
# Author:  Alex Stivala
# Created: May 2020
#
"""Python implementation of the Robbins-Monro Stochastic
 Approximation algorithm for estimation of Autologistic Actor
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


 The example data is described in:

  Stivala, A. D., Gallagher, H. C., Rolls, D. A., Wang, P., & Robins,
  G. L. (2020). Using Sampled Network Data With The Autologistic Actor
  Attribute Model. arXiv preprint arXiv:2002.00849.

"""

import time
import os
import sys
import random
import math
import numpy as np         # used for matrix & vector data types and functions
from functools import partial

from utils import int_or_na,NA_VALUE
from Graph import Graph
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
from changeStatisticsALAAM import *
from changeStatisticsALAAMbipartite import *
from stochasticApproximation import stochasticApproximation
from computeObservedStatistics import computeObservedStatistics
from gofALAAM import gof
from basicALAAMsampler import basicALAAMsampler
from bipartiteALAAMsampler import bipartiteALAAMsampler
from simulateALAAM import rand_bin_array


def run_on_network_attr(edgelist_filename, param_func_list, labels,
                        outcome_bin_filename,
                        binattr_filename=None,
                        contattr_filename=None,
                        catattr_filename=None,
                        sampler_func = basicALAAMsampler,
                        zone_filename = None,
                        directed = False,
                        bipartite = False,
                        GoFiterationInStep = 1000,
                        GoFburnIn = 10000,
                        bipartiteGoFfixedMode = None
                        ):
    """Run estimation using stochastic approximation algorithm
    on specified network with binary and/or continuous and
    categorical attributes.
    
    Parameters:
         edgelist_filename - filename of Pajek format edgelist 
         param_func_list   - list of change statistic functions corresponding
                             to parameters to estimate
         labels            - list of strings corresponding to param_func_list
                             to label output (header line)
         outcome_bin_filename - filename of binary attribute (node per line)
                                of outcome variable for ALAAM
         binattr_filename - filename of binary attributes (node per line)
                            Default None, in which case no binary attr.
         contattr_filename - filename of continuous attributes (node per line)
                            Default None, in which case no continuous attr.
         catattr_filename - filename of continuous attributes (node per line)
                            Default None, in which case no categorical attr.
         sampler_func        - ALAAM sampler function with signature
                               (G, A, changestats_func_list, theta, performMove,
                                sampler_m); see basicALAAMsampler.py
                               default basicALAAMsampler
         zone_filename   - filename of snowball sampling zone file 
                           (header line 'zone' then zone number for nodes,
                           one per line)
                           Default None, in which case no snowball zones.
                           If not None then the sampler_func should take
                           account of snowball sample zones i.e.
                           conditionalALAAMsampler()
         directed        - Default False. 
                           True for directed network else undirected.
         bipartite       - Default False.
                           True for two-mode network else one-mode.
         GoFiterationInStep - number of MCMC steps between each sample in GoF.
                              Default 1000.
         GoFburnIn         - number of iterations to discard at start for GoF.
                             Default 10000.
         bipartiteGoFfixedMode - for bipartite networks only, the mode
                                 (MODE_A or MODE_B that is fixed to NA
                                 in GoF simulation, for when outcome
                                 variable not defined for that mode,
                                 or None. Default None.

    Write output to stdout.

    """
    assert(len(param_func_list) == len(labels))
    assert bipartiteGoFfixedMode in [None, MODE_A, MODE_B]
    assert not (bipartiteGoFfixedMode is not None and not bipartite)
    assert not (zone_filename is not None and bipartite)

    if directed:
        if bipartite:
            raise Exception("directed bipartite network not suppored")
        G = Digraph(edgelist_filename, binattr_filename, contattr_filename,
                    catattr_filename, zone_filename)
    else:
        if bipartite:
            G = BipartiteGraph(edgelist_filename, binattr_filename,
                               contattr_filename, catattr_filename,
                               zone_filename)
        else:
            G = Graph(edgelist_filename, binattr_filename,
                      contattr_filename, catattr_filename, zone_filename)
        

    G.printSummary()

    outcome_binvar = list(map(int_or_na, open(outcome_bin_filename).read().split()[1:]))
    assert(len(outcome_binvar) == G.numNodes())
    A = outcome_binvar

    assert( all([x in [0,1,NA_VALUE] for x in A]) )
    print('positive outcome attribute = ', (float(A.count(1))/len(A))*100.0, '%')
    if NA_VALUE in A:
        print('Warning: outcome variable has', A.count(NA_VALUE), 'NA values')

    # Calculate observed statistics by summing change stats for each 1 variable
    Zobs = computeObservedStatistics(G, A, param_func_list)
    print('Zobs = ', Zobs)

    theta = np.zeros(len(param_func_list))

    estimation_start = time.time()
    max_runs = 20
    i = 0
    converged = False
    while i < max_runs and not converged:
        i += 1
        print('Running stochastic approximation (run', i,' of at most',max_runs,')...')
        start = time.time()
        (theta, std_error, t_ratio) = stochasticApproximation(G, A,
                                                              param_func_list,
                                                              theta, Zobs,
                                                              sampler_func) 

        print('Stochastic approximation took',time.time() - start, 's')
        if theta is None:
            print('Failed.')
            break
        print('           ',labels)
        print('theta     =', theta)
        print('std_error =', std_error)
        print('t_ratio   =', t_ratio)

        converged = np.all(np.abs(t_ratio) < 0.1)

    print('Total estimation time (',i,'runs) was',time.time() - estimation_start, 's')
    if converged:
        print('Converged.')
        significant = np.abs(theta) > 2 * std_error
        sys.stdout.write(30*' ' + '  Parameter Std.Error t-ratio\n')
        for j in range(len(theta)):
            sys.stdout.write('%30.30s % 7.3f    % 7.3f    % 7.3f %c\n' % (labels[j], theta[j], std_error[j], t_ratio[j], ('*' if significant[j] else ' ')))
        print()

        # Do goodness-of-fit test

        # change stats functions to add to GoF if not already in estimation
        if directed:
            # TODO GoF statistics for directed
            gof_param_func_list = list(param_func_list)
            goflabels = list(labels)
        elif bipartite:
            # TODO better GoF statitsics for bipartite.
            # Note that some of these are the same as bipartite stats
            # usually used, e.g. changeThreeStar is bipartiteEgoThreeStar
            # etc. Note also cannot use the attribute or bipatite functions
            # here with functools.partial() as used in specifying model,
            # as partial() even with the same parameters will give a different
            # function address so the comparison "if f not in param_func_list"
            # will always be True.
            statfuncs = [changeTwoStar, changeThreeStar, changePartnerActivityTwoPath,
                         changeContagion,
                         changeIndirectPartnerAttribute,
                         changePartnerAttributeActivity,
                         changePartnerPartnerAttribute]
            statlabels = ['Two-Star', 'Three-Star', 'Alter-2Star1',
                          'Contagion', 'Alter-2Star2', 'Partner-Activity',
                          'Partner-Resource']
            gof_param_func_list = (list(param_func_list) +
                                   [f for f in statfuncs
                                if f not in param_func_list])
            goflabels = (list(labels) + [f for f in statlabels
                                     if f not in labels])
        else:
            statfuncs = [changeTwoStar, changeThreeStar, changePartnerActivityTwoPath,
                         changeTriangleT1, changeContagion,
                         changeIndirectPartnerAttribute,
                         changePartnerAttributeActivity,
                         changePartnerPartnerAttribute,
                         changeTriangleT2,
                         changeTriangleT3]
            statlabels = ['Two-Star', 'Three-Star', 'Alter-2Star1',
                          'T1', 'Contagion', 'Alter-2Star2', 'Partner-Activity',
                          'Partner-Resource','T2', 'T3']
            gof_param_func_list = (list(param_func_list) +
                                   [f for f in statfuncs
                                if f not in param_func_list])
            goflabels = (list(labels) + [f for f in statlabels
                                     if f not in labels])
        n = len(gof_param_func_list)
        assert len(goflabels) == n
        # pad theta vector with zeros for the added parameters
        gof_theta = np.array(list(theta) + (n-len(theta))*[0])

        Ainitial = None # default: use random intialization
        if zone_filename is not None: # 7onditional estimation
            # For snowball conditional estimation, we must not start with
            # random initial outcome vector, but rather make sure the
            # nodes in the outermost zone have the same outcome attributes
            # as the obseved vector
            Ainitial = np.copy(A) # copy of observed vector
            # make vector of 50% ones, size of number of inner nodes
            Arandom_inner = rand_bin_array(int(0.5*len(G.inner_nodes)), len(G.inner_nodes))
            # set the outcome for inner nodes to random values, leaving
            # value of outermost nodes at the original observed values
            Ainitial[G.inner_nodes] = Arandom_inner
        elif bipartite:
            if bipartiteGoFfixedMode == MODE_A:
                Ainitial = np.concatenate(
                         (rand_bin_array(int(0.5*G.num_A_nodes), G.num_A_nodes),
                          np.ones(G.num_B_nodes)*NA_VALUE) )
            elif bipartiteGoFfixedMode == MODE_B:
                Ainitial = np.concatenate(
                       np.ones(G.num_A_nodes)*NA_VALUE,
                       (rand_bin_array(int(0.5*G.num_B_nodes), G.num_B_nodes)) )
        print('Running goodness-of-fit test...')
        start = time.time()
        gofresult = gof(G, A, gof_param_func_list, gof_theta,
                        sampler_func = sampler_func, Ainitial = Ainitial,
                        iterationInStep = GoFiterationInStep,
                        burnIn = GoFburnIn)
        print('GoF took',time.time() - start, 's')
        print('           ',goflabels)
        print('t_ratios = ',gofresult)
        
        sys.stdout.write(30*' ' + '  t-ratio\n')
        for j in range(n):
            sys.stdout.write('%30.30s % 7.3f\n' % (goflabels[j], gofresult[j]))
        print()

        if isinstance(G, BipartiteGraph):
            print("twoPaths cache info: ", G.twoPaths.cache_info())
    
def run_example():
    """
    example run on simulated 500 node network
    """
    run_on_network_attr(
        '../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt',
        [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
        ["Density", "Activity", "Contagion", "Binary", "Continuous"],
        '../data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt',
        '../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt',
        '../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt'
    )


def run_bipartite_example():
    """
    example run on bipartite network
    """
    run_on_network_attr('../data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net',
                        [partial(changeBipartiteDensity, MODE_A),
                         partial(changeBipartiteActivity, MODE_A),
                         partial(changeBipartiteEgoTwoStar, MODE_A),
                         partial(changeBipartiteAlterTwoStar1,MODE_A),
                         partial(changeBipartiteAlterTwoStar2,MODE_A),
                         partial(changeBipartiteFourCycle1, MODE_A),
                         partial(changeBipartiteFourCycle2, MODE_A)],
                        ['bipartiteDensityA',
                         'bipartiteActivityA',
                         'bipartiteEgoTwoStarA',
                         'bipartiteAlterTwoStar1A',
                         'bipartiteAlterTwoStar2A',
                         'bipartiteFourCycle1A',
                         'bipartiteFourCycle2A'],
                        '../data/bipartite/Inouye_Pyke_pollinator_web/inouye_outcome_BNA.txt',
                        sampler_func = partial(bipartiteALAAMsampler, MODE_A),
                        bipartite=True)
