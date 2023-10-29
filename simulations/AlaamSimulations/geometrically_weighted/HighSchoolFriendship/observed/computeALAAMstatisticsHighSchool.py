#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsHighschool.py
# Author:  Alex Stivala
# Created: April 2023
#
"""Compute the observed statistics of specified ALAAM outcome vector
   and network and node attributes.
"""
import sys
import numpy as np         # used for matrix & vector data types and functions
from math import log
from functools import partial
from Graph import Graph
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph
from utils import int_or_na
from computeObservedStatistics import computeObservedStatistics
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity,param_func_to_label


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
    labels += ['meanInDegree1', 'varInDegree1', 'meanOutDegree1', 'varOutDegree1', 'meanInDegree0', 'varInDegree0', 'meanOutDegree0', 'varOutDegree0']
    indegseq = np.array([G.indegree(v) for v in iter(G.G.keys())])
    outdegseq = np.array([G.outdegree(v) for v in iter(G.G.keys())])
    A = np.array(outcome_binvar)
    ## mean and variance of degrees of nodes with outcome = 1
    meanInDegree1 = np.mean(indegseq[np.nonzero(A == 1)[0]])
    varInDegree1 = np.var(indegseq[np.nonzero(A == 1)[0]])
    meanOutDegree1 = np.mean(outdegseq[np.nonzero(A == 1)[0]])
    varOutDegree1 = np.var(outdegseq[np.nonzero(A == 1)[0]])
    ## mean and variance of degrees of nodes with outcome = 0
    meanInDegree0 = np.mean(indegseq[np.nonzero(A == 0)[0]])
    varInDegree0 = np.var(indegseq[np.nonzero(A == 0)[0]])
    meanOutDegree0 = np.mean(outdegseq[np.nonzero(A == 0)[0]])
    varOutDegree0 = np.var(outdegseq[np.nonzero(A == 0)[0]])

    Zobs = np.append(Zobs, [meanInDegree1, varInDegree1, meanOutDegree1, varOutDegree1])
    Zobs = np.append(Zobs, [meanInDegree0, varInDegree0, meanOutDegree0, varOutDegree0])

    sys.stdout.write(' '.join(labels) + '\n')
    sys.stdout.write(' '.join([str(z) for z in Zobs]) + '\n')



##
## main
##

param_func_list  =  [changeDensity, changeSender, changeReceiver, changeContagion, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar,  changeContagionReciprocity, changeAlterOutTwoStar2, changeTransitiveTriangleT1, changeTransitiveTriangleT3, partial(changeGWSender, log(2.0)),  partial(changeGWReceiver, log(2.0)), partial(changeGWContagion, log(2.0)), changeLogContagion]

get_observed_stats_from_network_attr(
        '../../../HighSchoolFriendship/data/highschool_friendship_arclist.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        '../../../HighSchoolFriendship/data/highschool_friendship_binattr.txt', # outcome gender=male
        directed = True
)
