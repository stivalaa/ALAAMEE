#!/usr/bin/env python
#
# File:    changeStatisticsALAAM.py
# Author:  Alex Stivala
# Created: February 2020
#
"""Functions to compute change statistics for ALAAM. Each function takes a Graph
G and outcome vector A and returns the change statistic for changing
outcome of node i to 1.

The change statistics here are documented in Daraganova & Robins
(2013) Tables 9.1 - 9.3 (pp. 110-112) and the PNet manual Appendix B
"IPNet Graph Statistics" (pp. 42-43), and here I use a similar naming
convention to the latter. Similarly, the diagrams will follow a
similar convention where a black or solid node, shown as an asterisk
"*" here, denotes an actor with the outcome attribute, while a hollow
or white node, shown as an uppercase "O" here, denotes an actor with
or without the attribute.

See

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.

  Wang, P., Robins, G., & Pattison, P. (2009). PNet: A program for the
  simulation and estimation of exponential random graph
  models. University of Melbourne.

"""

import math

from Graph import Graph


def changeDensity(G, A, i):
    """
    change statistic for [outcome attribute] Density

    *
    """
    return 1


def changeActivity(G, A, i):
    """
    change statistic for Activity

    *--O
    """
    return G.degree(i)


def changeContagion(G, A, i):
    """
    change statistic for Contagion (partner attribute)

    *--*
    """
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] != 0:
            delta += 1
    return delta


def changeoOb(G, A, i):
    """change statistic for binary exogenous attribute oOb (outcome
    attribute related to binary attribute on same node)

    [*]
    """
    return G.binattr[i]


def changeoOc(G, A, i):
    """change statistic for continuous exogenous attribute oOc (outcome
    attribute related to continuous attribute on same node)

    (*)
    """
    return G.contattr[i]



