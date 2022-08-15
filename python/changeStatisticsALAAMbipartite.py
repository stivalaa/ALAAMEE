#!/usr/bin/env python3
#
# File:    changeStatisticsALAAMbipartite.py
# Author:  Alex Stivala
# Created: August 2022
#
"""Functions to compute change statistics for ALAAM on bipartite
(two-mode) graphs (undirected). Each function takes a BipartiteGraph G and
outcome vector A and returns the change statistic for changing outcome
of node i to 1.

These functions take as their first parameter the type (mode) of the
node, either MODE_A or MODE_B (defined in BipartiteGraph.py).  So that
these functions have the same signature as the structural statistics,
use functools.partial() to create a function with the (G, A, i)
signature, e.g. partial(changeBipartiteDensity(MODE_B).

The attribute statistics take also as their second parameter the name
of the attribute to use, used as the key in the relevant attribute
dictionary in the Graph object. As described in
changeStatisticsALAAM.py, functools.partial() is also used to create a
function wih the (G, A, i) signature. Similarly for functions that
take a setting network, as also described in changeStatisticsALAAM.py.

In the function documentation here, a black or solid node, shown as an
asterisk "*" here, denotes an actor with the outcome attribute, while
a hollow or white node, shown as an lowercase "o" here, denotes an
actor with or without the attribute.

See

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.

  Wang, P., Robins, G., & Pattison, P. (2009). PNet: A program for the
  simulation and estimation of exponential random graph
  models. University of Melbourne. http://www.melnet.org.au/s/PNetManual.pdf

  Wang, P., Robins, G., Pattison, P., & Koskinen, J. (2014). MPNet: A
  program for the simulation and estimation of exponential random
  graph models for multilevel networks. University of
  Melbourne. http://www.melnet.org.au/s/MPNetManual.pdf

  Wang, P., Stivala, A., Robins, G.,Pattison, P., Koskinen, J., &
  Lomi, A. (2022) PNet: Program for the simulation and estimation of
  exponential random graph models for multilevel networks.
  http://www.melnet.org.au/s/MPNetManual2022.pdf

"""

import math

from utils import NA_VALUE
from BipartieGraph import BipartiteGraph

def changeBipartiteDensity(mode, G, A, i):
    """
    change statistic for [outcome attribute] Density

    *
    """
    return 1 if G.bipartite_node_mode(i) == mode else 0


def changeBipartiteActivity(mode, G, A, i):
    """
    change statistic for Activity

    *--o
    """
    return G.degree(i) if G.bipartite_node_mode(i) == mode else 0

