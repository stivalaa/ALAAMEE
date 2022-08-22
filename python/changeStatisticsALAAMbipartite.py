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
signature, e.g. partial(changeBipartiteDensity, MODE_B).

The attribute statistics take also as their second parameter the name
of the attribute to use, used as the key in the relevant attribute
dictionary in the Graph object. As described in
changeStatisticsALAAM.py, functools.partial() is also used to create a
function wih the (G, A, i) signature. Similarly for functions that
take a setting network, as also described in changeStatisticsALAAM.py.

In the function documentation here, a node shown as an asterisk "*"
here, denotes a node of the specified mode with the outcome attribute,
and if shown as "@" is a node of the other mode with the outcome
attibute.

A node shown as an lowercase "o" here, denotes a node of the other
(non-reference) node with or without the attribute, and a node shown
as lowercase "x" is an actor of the reference mode with or without the
outcome attribute. In summary:


 Mode       Outcome variable       Symbol
 =  mode    0 or 1                 x
 =  mode    1                      *
 != mode    0 or 1                 o
 != mode    1                      @

(The symbols are chosen so that * is a bit like a 'filled' x, and @ is a
bit like a 'filled' o).

Note since the network is bipartite, only nodes of different modes can
have an edge between them, i.e. we can have *--o, *--@, x--o, and
x--@, but not *--*, *--x, o--o, or o--@.

So in the functions, a node denoted * is the node i, which has the
supplied (reference) mode and is being changed from 0 to 1 on the
outcome variable. (Note there may be more than one such node, in which
case they will be structurally equivalent). So all the functions will
return 0 if the mode of node i is not equal to the supplied reference
mode.

The use of the mode parameter and functools.partial() avoids having to
implement two versions of every funciton, one for each mode. E.g.
instead of having to define both changeBipartiteActivityA(G, A, i) and
changeBipartiteActivityB(G, A, i) which check that G.bipartite_node_mode(i) ==
MODE_A and G.bipartite_node_mode(i) == MODE_B, respectively, we just
have the single function changeBipartiteActivity(mode, G, A, i), which
we can use via partial(changeBipartiteActivity, MODE_A) or
partial(changeBipartiteActivity, MODE_B).

The function documentaiton also shows the MPNet name for the
statistic, with [mode] for the relevant mode.
E.g. partial(changeBipartiteDensity, MODE_A) means density for node
type A, DesnityXA in MPNet.


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
from BipartiteGraph import BipartiteGraph
import changeStatisticsALAAM


def changeBipartiteDensity(mode, G, A, i):
    """
    change statistic for bipartite [outcome attribute] Density
    DensityX[mode]

    *
    """
    return 1 if G.bipartite_node_mode(i) == mode else 0


def changeBipartiteActivity(mode, G, A, i):
    """
    change statistic for bipartite Activity
    ActivityX[mode]

    *--o
    """
    return G.degree(i) if G.bipartite_node_mode(i) == mode else 0


def changeBipartiteEgoTwoStar(mode, G, A, i):
    """
    Change statistic for bipartite ego two-star
    EgoX-2Star[mode]

    o--*--o
    """
    return (changeStatisticsALAAM.changeTwoStar(G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)


def changeBipartiteAlterTwoStar1(mode, G, A, i):
    """
    Change statistic for bipartite alter two-star 1
    AlterX-2Star1[mode]

    x--o--*
    """
    return (changeStatisticsALAAM.changePartnerActivityTwoPath(G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)

def changeBipartiteAlterTwoStar2(mode, G, A, i):
    """
    Change statistic for bipartite alter two-star 2
    AlterX-2Star2[mode]

    *--o--*
    """
    return (changeStatisticsALAAM.changeIndirectPartnerAttribute(G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)


def changeBipartiteFourCycle1(mode, G, A, i):
    """
    Change setatistic for bipartite four-cycle 1
    C4X-1[mode]

        o
       / \
      x   *
       \ /
        o
    """
    if G.bipartite_node_mode(i) == mode:
        delta = 0
        for v in G.nodeModeIterator(mode):
            twoPathCount = G.twoPaths(i, v)
            delta += twoPathCount * (twoPathCount - 1) / 2
        return delta
    else:
        return 0
