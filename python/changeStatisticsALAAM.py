#!/usr/bin/env python
#
# File:    changeStatisticsALAAM.py
# Author:  Alex Stivala
# Created: February 2020
#
"""Functions to compute change statistics for ALAAM. Each function takes a Graph
G and outcome vector A and returns the change statistic for changing
outcome of node i to 1.

See

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.

"""

import math

from Graph import Graph


def changeDensity(G, A, i):
    """
    change statistic for [outcome attribute] Density
    """
    return 1


def changeActivity(G, A, i):
    """
    change statistic for Activity
    """
    return G.degree(i)


def changeContagion(G, A, i):
    """
    change statistic for Contagion
    """
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] != 0:
            delta += 1
    return delta


def changeoOb(G, A, i):
    """
    change statistic for binary attribute oOb (outcome attribute related to
    binary attribute on same node)
    """
    return G.binattr[i]


def changeoOc(G, A, i):
    """
    change statistic for continuous attribute oOc (outcome attribute related to
    continuous attribute on same node)
    """
    return G.contattr[i]



