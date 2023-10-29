#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsGitHub.py
# Author:  Alex Stivala
# Created: August 2023
#
"""Compute the observed statistics of specified ALAAM outcome vector
   and network and node attributes.
"""
import sys
import numpy as np         # used for matrix & vector data types and functions
from functools import partial
from math import log
from Graph import Graph
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph
from utils import int_or_na
from computeObservedStatistics import computeObservedStatistics
from changeStatisticsALAAM import *



def get_observed_stats_from_network_attr(edgelist_filename, param_func_list,
                                         labels,
                                         outcome_bin_filename,
                                         binattr_filename=None,
                                         contattr_filename=None,
                                         catattr_filename=None,
                                         directed=False,
                                         bipartite=False):
    """Compute observed stats for outcome on specified network with binary
    and/or continuous and categorical attributes.

    Parameters:
         edgelist_filename - filename of Pajek format edgelist
         param_func_list   - list of change statistic functions corresponding
                             to statistics to compute
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
         directed        - Default False.
                           True for directed network else undirected.
         bipartite       - Default False.
                           True for two-mode network else one-mode.

    Write output to stdout in format readable by R script
    plotSimulationDiagnostics.R

    """
    assert(len(param_func_list) == len(labels))


    if directed:
        if bipartite:
            raise Exception("directed bipartite network not suppored")
        G = Digraph(edgelist_filename, binattr_filename, contattr_filename,
                    catattr_filename)
    else:
        if bipartite:
            G = BipartiteGraph(edgelist_filename, binattr_filename,
                               contattr_filename, catattr_filename)
        else:
            G = Graph(edgelist_filename, binattr_filename,
                      contattr_filename, catattr_filename)


    outcome_binvar = list(map(int_or_na, open(outcome_bin_filename).read().split()[1:]))
    assert(len(outcome_binvar) == G.numNodes())
    A = outcome_binvar

    assert( all([x in [0,1,NA_VALUE] for x in A]) )

    # Calculate observed statistics by summing change stats for each 1 variable
    Zobs = computeObservedStatistics(G, A, param_func_list)

    ## Add mean and variance of degrees of nodes with different outcome values
    labels += ['meanDegree1', 'varDegree1', 'meanDegree0', 'varDegree0']
    degseq = np.array([G.degree(v) for v in G.nodeIterator()])
    A = np.array(outcome_binvar)
    ## mean and variance of degrees of nodes with outcome = 1
    meanDegree1 = np.mean(degseq[np.nonzero(A == 1)[0]])
    varDegree1 = np.var(degseq[np.nonzero(A == 1)[0]])
    ## mean and variance of degrees of nodes with outcome = 0
    meanDegree0 = np.mean(degseq[np.nonzero(A == 0)[0]])
    varDegree0 = np.var(degseq[np.nonzero(A == 0)[0]])

    Zobs = np.append(Zobs, [meanDegree1, varDegree1, meanDegree0, varDegree0])

    sys.stdout.write(' '.join(labels) + '\n')
    sys.stdout.write(' '.join([str(z) for z in Zobs]) + '\n')




##
## main
##
param_func_list = [changeDensity, changeActivity, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeContagion, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute, changeTriangleT1, changeTriangleT2, changeTriangleT3, partial(changeGWActivity, log(2.0)), partial(changeGWContagion, log(2.0)), changeLogContagion]

get_observed_stats_from_network_attr(
        '../../../GitHubSimulations/data/musae_git.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        '../../../GitHubSimulations/data/musae_git_target.txt'
)
