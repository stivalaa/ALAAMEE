#
# File:    simualateALAAMsimpleDemo.py
# Author:  Alex Stivala
# Created: May 2020
#
"""Simple demonstration of ALAAM simulation (generating binary outcome
   vectors given network, node attributes, ALAAM mode parmaters).

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
import math
import numpy as np         # used for matrix & vector data types and functions
from functools import partial

from Graph import Graph,NA_VALUE,int_or_na
from changeStatisticsALAAM import *
from simulateALAAM import simulateALAAM

def simulate_from_network_attr(edgelist_filename, param_func_list, labels,
                               theta,
                               binattr_filename=None,
                               contattr_filename=None,
                               catattr_filename=None):
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

    """
    assert(len(param_func_list) == len(labels))

    G = Graph(edgelist_filename, binattr_filename, contattr_filename,
              catattr_filename)

    G.printSummary()
    
    for simvec in simulateALAAM(G, param_func_list, theta, numSamples = 100):
        print simvec #XXX
    

def run_example():
    """
    example run on simulated 500 node network
    """
    simulate_from_network_attr(
        '../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt',
        [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
        ["Density", "Activity", "Contagion", "Binary", "Continuous"],
        np.array([-7.2, 0.55, 1.0, 1.2, 1.5]),
        '../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt',
        '../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt'
    )
