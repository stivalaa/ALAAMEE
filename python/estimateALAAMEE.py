#
# File:    estimateALAAMEE.py
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


 The example data is described in:

  Stivala, A. D., Gallagher, H. C., Rolls, D. A., Wang, P., & Robins,
  G. L. (2020). Using Sampled Network Data With The Autologistic Actor
  Attribute Model. arXiv preprint arXiv:2002.00849.

"""

import time
import os
import random
import math
import numpy as np         # used for matrix & vector data types and functions
from functools import partial

from utils import NA_VALUE,int_or_na
from Graph import Graph
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph
from changeStatisticsALAAM import *
from initialEstimator import algorithm_S
#OLD:from equilibriumExpectation import algorithm_EE,THETA_PREFIX,DZA_PREFIX
from equilibriumExpectationBorisenko import algorithm_EE,THETA_PREFIX,DZA_PREFIX
from basicALAAMsampler import basicALAAMsampler


def run_on_network_attr(edgelist_filename, param_func_list, labels,
                        outcome_bin_filename,
                        binattr_filename=None,
                        contattr_filename=None,
                        catattr_filename=None,
                        EEiterations    = 50000,
                        run = None,
                        learningRate = 0.01,
                        sampler_func = basicALAAMsampler,
                        zone_filename= None,
                        directed = False,
                        bipartite = False):
    """Run estimation using EE algorithm on specified network with binary 
    and/or continuous and categorical attributes.
    
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
         catattr_filename - filename of categorical attributes (node per line)
                            Default None, in which case no categorical attr.
         EEiterations     - Number of iterations of the EE algorithm.
                            Default 50000.
         run              - run number for parallel runs, used as suffix on 
                            output filenames. Default None
                            in which case no suffix added to output files.
         learningRate        - learning rate (step size multiplier, a)
                               defult 0.01
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



    Write output to ifd_theta_values_<basename>_<run>.txt and
                    ifd_dzA_values_<basename>_<run>.txt
    where <basename> is the baesname of edgelist filename e..g
    if edgelist_filename is edges.txt then ifd_theta_values_edges_0.txt
    and ifd_dzA_values_edges_0.txt etc.
    WARNING: these files are overwritten.

    """
    assert(len(param_func_list) == len(labels))
    basename = os.path.splitext(os.path.basename(edgelist_filename))[0]
    THETA_OUTFILENAME = THETA_PREFIX + basename
    DZA_OUTFILENAME = DZA_PREFIX + basename
    if run is not None:
        THETA_OUTFILENAME += '_' + str(run)
        DZA_OUTFILENAME += '_' + str(run)
    THETA_OUTFILENAME += os.extsep + 'txt'
    DZA_OUTFILENAME   += os.extsep + 'txt'

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
    print('positive outcome attribute = ', (float(A.count(1))/len(A))*100.0, '%')
    assert( all([x in [0,1,NA_VALUE] for x in A]) )

    if NA_VALUE in A:
        print('Warning: outcome variable has', A.count(NA_VALUE), 'NA values')

    A = np.array(A) # convert list to numpy vector
    
    # steps of Alg 1    
    M1 = 100

    #OLD: Mouter = 500 # outer iterations of Algorithm EE
    #OLD: Msteps = 100 # multiplier for number of inner steps of Algorithm EE
    #OLD: print 'M1 = ', M1, ' Mouter = ', Mouter, ' Msteps = ', Msteps

    print('M1 = ', M1, ' EEiterations = ', EEiterations, end=' ') 
    print('learningRate = ', learningRate, end=' ')
    
    theta_outfile = open(THETA_OUTFILENAME, 'w',1) # 1 means line buffering
    theta_outfile.write('t ' + ' '.join(labels) + ' ' + 'AcceptanceRate' + '\n')
    print('Running Algorithm S...', end=' ')
    start = time.time()
    (theta, Dmean) = algorithm_S(G, A, param_func_list, M1, theta_outfile,
                                 sampler_func)
    print(time.time() - start, 's')
    print('after Algorithm S:')
    print('theta = ', theta)
    print('Dmean = ', Dmean)
    dzA_outfile = open(DZA_OUTFILENAME, 'w',1)
    dzA_outfile.write('t ' + ' '.join(labels) + '\n')
    print('Running Algorithm EE...', end=' ')
    start = time.time()
    #OLD: theta = algorithm_EE(G, A, param_func_list, theta, Dmean,
    #OLD:                     Mouter, Msteps, theta_outfile, dzA_outfile)
    theta = algorithm_EE(G, A, param_func_list, theta, 
                         EEiterations, theta_outfile, dzA_outfile, learningRate,
                         sampler_func)

    print(time.time() - start, 's')
    theta_outfile.close()
    dzA_outfile.close()
    print('at end theta = ', theta)

    print
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
