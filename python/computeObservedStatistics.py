#
# File:    computeObseervedStatistics.py
# Author:  Alex Stivala
# Created: May 2020
#
"""
Compute the observed values of ALAAM statistics by summing the change
statistics for each 1 variable in the outcome variable vector.
"""
import sys
import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph,NA_VALUE
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph
from utils import int_or_na
from changeStatisticsALAAM import *


def computeObservedStatistics(G, Aobs, changestats_func_list):
    """
    Compute the observed values of ALAAM statistics by summing the change
    statistics for each 1 variable in the outcome variable vector.
    
    Parameters:
       G                   - Graph object for graph to compute stats in
       Aobs                - vector of 0/1 outcome variables for ALAAM
       changestats_func_list-list of change statistics funcions

     Returns:
        numpy vector of observed statistics corresponding to the 
        cangestats_func_list

    """
    # Calculate observed statistics by summing change stats for each 1 variable
    n = len(changestats_func_list)
    Zobs = np.zeros(n)
    Acopy = np.zeros(len(Aobs))
    for i in range(len(Aobs)):
        if Aobs[i] == NA_VALUE:
            Acopy[i] = NA_VALUE
        if Aobs[i] == 1:
            for l in range(n):
                Zobs[l] += changestats_func_list[l](G, Acopy, i)
            Acopy[i] = 1
    assert(np.all(Acopy == Aobs))
    return Zobs



def get_observed_stats_from_network_attr(edgelist_filename, param_func_list,
                                         labels,
                                         outcome_bin_filename,
                                         binattr_filename=None,
                                         contattr_filename=None,
                                         catattr_filename=None,
                                         directed=False,
                                         bipartite=False,
                                         degreestats=False):
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
         degreestats     - Default False.
                           If True then also compute mean and variance
                           of nodes with outcome variable = 1 (and also 0).

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

    if degreestats:
        ## Add mean and variance of degrees of nodes with different
        ## outcome values
        ## TODO directed and bipartite degrees
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
