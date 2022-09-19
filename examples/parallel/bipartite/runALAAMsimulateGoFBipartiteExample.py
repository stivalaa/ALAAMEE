#!/usr/bin/env python3
#
# File:    run runALAAMsimualteGoFBipartiteExample.py
# Author:  Alex Stivala
# Created: September 2022
#
"""Simuilate bipartite Autologistic Actor Attribute Model (ALAAM).
"""
import sys
from functools import partial
import numpy as np

from changeStatisticsALAAM import *
from changeStatisticsALAAMbipartite import *
from BipartiteGraph import MODE_A,MODE_B
from bipartiteALAAMsampler import bipartiteALAAMsampler
from basicALAAMsampler import basicALAAMsampler
from simulateALAAM import simulateALAAM,rand_bin_array
from Graph import int_or_na

def simulate_from_network_attr(edgelist_filename, param_func_list, labels,
                               theta,
                               binattr_filename=None,
                               contattr_filename=None,
                               catattr_filename=None,
                               sampler_func = basicALAAMsampler,
                               numSamples = 100,
                               iterationInStep = None,
                               burnIn = None):
    """Simulate ALAAM from on specified network with binary and/or continuous
    and categorical attributes.
    
    Parameters:
         edgelist_filename - filename of Pajek format edgelist 
         param_func_list   - list of change statistic functions corresponding
                             to parameters to estimate
         labels            - list of strings corresponding to param_func_list
                             to label output (header line)
         theta             - correponding vector of theta values
         binattr_filename - filename of binary attributes (node per line)
                            Default None, in which case no binary attr.
         contattr_filename - filename of continuous attributes (node per line)
                            Default None, in which case no continuous attr.
         catattr_filename - filename of categorical attributes (node per line)
                            Default None, in which case no categorical attr.
         sampler_func        - ALAAM sampler function with signature
                               (G, A, changestats_func_list, theta, performMove,
                                sampler_m); see basicALAAMsampler.py
                               default basicALAAMsampler
         iterationInStep  - number of sampler iterations
                             i.e. the number of iterations between samples
                             (or 10*numNodes if None)
         numSamples       - Number of samples (default 100)
         burnIn           - Number of sampels to discard at start
                            (or 10*iterationInStep if None)


    """
    assert(len(param_func_list) == len(labels))


    G = BipartiteGraph(edgelist_filename, binattr_filename, contattr_filename,
              catattr_filename)

    #G.printSummary()

    # for bipartite graph, make sure initial outcome vector is all NA for the
    # B mode (assuming we are using outcome only on A mode here)
    # and 0 or 1 with uniform probability for A mode
    Ainitial = np.concatenate(
                      (rand_bin_array(int(0.5*G.num_A_nodes), G.num_A_nodes),
                       np.ones(G.num_B_nodes)*NA_VALUE) )

    # now putting NA in initial value where NA in observed to test
    outcome_bin_filename = '../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_outcome_BNA.txt'
    outcome_binvar = list(map(int_or_na, open(outcome_bin_filename).read().split()[1:]))
    assert(len(outcome_binvar) == G.numNodes())
    Ainitial[np.where(outcome_binvar == NA_VALUE)[0]] = NA_VALUE

    assert all(Ainitial[G.num_A_nodes:] == NA_VALUE)

    sys.stdout.write(' '.join(['t'] + labels + ['acceptance_rate']) + '\n')
    for (simvec,stats,acceptance_rate,t) in simulateALAAM(G, param_func_list,
                                                          theta,
                                                          numSamples,
                                                          iterationInStep,
                                                          burnIn,
                                                          sampler_func = sampler_func,
                                                          Ainitial = Ainitial):
        sys.stdout.write(' '.join([str(t)] + [str(x) for x in list(stats)] +
                                  [str(acceptance_rate)]) + '\n')
    

###
### Main
###

# parameters and corresponding labels 
# TODO parse from estimation output
param_func_list = [partial(changeBipartiteDensity, MODE_A),
     partial(changeBipartiteActivity, MODE_A),
     partial(changeBipartiteEgoTwoStar, MODE_A),
     partial(changeBipartiteEgoThreeStar, MODE_A),
     partial(changeBipartiteAlterTwoStar1,MODE_A),
     partial(changeBipartiteAlterTwoStar2,MODE_A),
     partial(changeBipartiteFourCycle1, MODE_A),
     partial(changeBipartiteFourCycle2, MODE_A)]
labels = ['bipartiteDensityA',
     'bipartiteActivityA',
     'bipartiteEgoTwoStarA',
     'bipartiteEgoThreeStarA',
     'bipartiteAlterTwoStar1A',
     'bipartiteAlterTwoStar2A',
     'bipartiteFourCycle1A',
     'bipartiteFourCycle2A']

# estimation results from 
#alaamee_bipartite_inouye-1294073.out
#Pooled
#bipartiteDensityA -0.8438772 0.06705921 2.875851 0.0255977  
#bipartiteActivityA 0.8107591 0.06806219 2.075133 0.003936713  
#bipartiteEgoTwoStarA -0.09686201 0.01183513 0.2645885 0.01838947  
#bipartiteAlterTwoStar1A -0.0254424 0.01350741 0.2970958 0.02542292  
#bipartiteAlterTwoStar2A -0.04803535 0.02747076 0.7133797 0.0677331  
#bipartiteFourCycle1A 0.05426511 0.01329 0.2117922 0.004779611  
#bipartiteFourCycle2A -0.08229107 0.02450527 0.4169688 0.1250154  
#TotalRuns 20 
#ConvergedRuns 20 
# TODO parse these from estimation output
theta = np.array([-0.8438772, 0.8107591, -0.09686201, 0, -0.0254424, -0.04803535, 0.05426511, -0.08229107])

###print('XXX', len(param_func_list), len(labels), len(theta))
gof_param_func_list = param_func_list
goflabels = labels
gof_theta = theta
n = len(gof_param_func_list)
assert len(goflabels) == n
assert len(theta) == n


simulate_from_network_attr(
    '../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net',
    gof_param_func_list,
    goflabels, 
    gof_theta,
    '../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_binattr.txt',
    '../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_contattr.txt',
    '../../data/bipartite/Inouye_Pyke_pollinator_web/inouye_catattr.txt',
     sampler_func = partial(bipartiteALAAMsampler, MODE_A),
     iterationInStep = 1000,
     burnIn = 1000
    )



