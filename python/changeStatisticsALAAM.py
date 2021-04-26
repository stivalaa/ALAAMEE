#!/usr/bin/env python3
#
# File:    changeStatisticsALAAM.py
# Author:  Alex Stivala
# Created: February 2020
#
"""Functions to compute change statistics for ALAAM. Each function takes a Graph
G and outcome vector A and returns the change statistic for changing
outcome of node i to 1.

The attribute statistics take also as their first parameter the name of 
the attribute to use, used as the key in the relevant attribute dictionary
in the Graph object. So that these functions have the same signature as
the structural statistics, use functools.partial() to create a function
with the (G, A, i) signature, e.g. partial(changeo_Oc, "age").
Similarly for the use of the setting network (another fixed graph for
different relationships than the main graph G) the setting-homophily
change statistic is used as e.g. partial(changeSettingHomophily, Gsetting).

The change statistics here are documented in Daraganova & Robins
(2013) Tables 9.1-9.3 (pp. 110-112) and the PNet manual Appendix B
"IPNet Graph Statistics" (pp. 42-43), and here I use a similar naming
convention to the latter. Similarly, the diagrams will follow a
similar convention where a black or solid node, shown as an asterisk
"*" here, denotes an actor with the outcome attribute, while a hollow
or white node, shown as an lowercase "o" here, denotes an actor with
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

from Graph import Graph,NA_VALUE


def changeDensity(G, A, i):
    """
    change statistic for [outcome attribute] Density

    *
    """
    return 1


def changeActivity(G, A, i):
    """
    change statistic for Activity

    *--o
    """
    return G.degree(i)


def changeTwoStar(G, A, i):
    """
    Change statistic for two-star

    *--o
     \
      o
    """
    return (G.degree(i) * (G.degree(i) - 1))/2.0 if G.degree(i) > 1 else 0


def changeThreeStar(G, A, i):
    """
    Change statistic for three-star

      o
     /
    *--o
     \
      o
    """
    return ( G.degree(i) * (G.degree(i) - 1) * (G.degree(i) - 2) / 6.0
             if G.degree(i) > 2 else 0 )
        

def changePartnerActivityTwoPath(G, A, i):
    """
    Change statistic for partner activity actor two-path (Alter-2Star1A)

    *--o--o
    """
    delta = 0
    for u in G.neighbourIterator(i):
        delta += G.degree(i) + G.degree(u) - 2
    return delta
    

def changeTriangleT1(G, A, i):
    """
    Change statistic for actor triangle (T1)

      o
     / \
    *---o
    """
    delta = 0
    if G.degree(i) < 2:
        return 0
    else:
        for u in G.neighbourIterator(i):
            for v in G.neighbourIterator(u):
                if v != i and G.isEdge(i, v):
                    delta += 1
    assert delta % 2 == 0
    return delta / 2.0
        

def changeContagion(G, A, i):
    """
    change statistic for Contagion (partner attribute)

    *--*
    """
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] == 1:
            delta += 1
    return delta


def changeIndirectPartnerAttribute(G, A, i):
    """
    Change statistic for indirect partner attribute (Alter-2Star2A);
    structural equivalence between actors with attribute (two-path equivalence)

    *--o--*
    """
    delta = 0
    for u in G.neighbourIterator(i):
        for v in G.neighbourIterator(u):
            if v != i and A[v] == 1:
                delta += 1
    return delta


def changePartnerAttributeActivity(G, A, i):
    """Change statistic for partner attribute activity (NB called
    "Partner-Activity" in PNet manual IPNet graph statistics (p. 42))

    *--*--o

    """
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] == 1:
            delta += G.degree(i) + G.degree(u) - 2
    return delta
    

# def changePartnerPartnerAttribute_OLD(G, A, i):
#     """
#     Change statistic for partner-partner-attribute (partner-resource)

#     *--*--*
#     """
#     delta = 0
#     for u in G.neighbourIterator(i):
#         if A[u] == 1:
#             # FIXME this is inefficient, iterating over all nodes
#             for v in range(G.numNodes()):
#                 if v == i or v == u:
#                     continue
#                 if A[v] == 1:
#                     if G.isEdge(u, v):
#                         delta += 2
#                     if G.isEdge(i, v):
#                         delta += 1
#     return delta


def changePartnerPartnerAttribute(G, A, i):
    """
    Change statistic for partner-partner-attribute (partner-resource)

    *--*--*
    """
#    delta_OLD = changePartnerPartnerAttribute_OLD(G, A, i)
    
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] == 1:
            for v in G.neighbourIterator(u):
                if A[v] == 1:
                    delta += 2
            for v in G.neighbourIterator(i):
                if A[v] == 1 and v != u:
                    delta += 1
                    
#    assert delta == delta_OLD
    return delta


def changeTriangleT2(G, A, i):
    """
    Change statistic for partner attribute triangle (T2)

      *
     / \
    *---o
    """
    delta = 0
    if G.degree(i) < 2:
        return 0
    else:
        for u in G.neighbourIterator(i):
            if A[u] == 1:
                for v in G.neighbourIterator(u):
                    if v != i and G.isEdge(i, v):
                        delta += 1
    return delta
        

def changeTriangleT3(G, A, i):
    """
    Change statistic for partner-partner attribute triangle (T3)

      *
     / \
    *---*
    """
    delta = 0
    if G.degree(i) < 2:
        return 0
    else:
        for u in G.neighbourIterator(i):
            if A[u] == 1:
                for v in G.neighbourIterator(u):
                    if v != i and A[v] == 1 and G.isEdge(i, v):
                        delta += 1
    assert delta % 2 == 0
    return delta / 2.0
        


def changeoOb(attrname, G, A, i):
    """change statistic for binary exogenous attribute oOb (outcome
    attribute related to binary attribute on same node)

    [*]
    """
    return 0 if G.binattr[attrname][i] == NA_VALUE else G.binattr[attrname][i]


def changeo_Ob(attrname, G, A, i):
    """change statistic for binary exogenous partner attribute o_Ob (outcome
    attribute related to binary attribute on partner node)

    *--[o]
    """
    delta = 0
    for u in G.neighbourIterator(i):
        delta += 0 if G.binattr[attrname][i] == NA_VALUE else G.binattr[attrname][u]
    return delta


def changeoOc(attrname, G, A, i):
    """change statistic for continuous exogenous attribute oOc (outcome
    attribute related to continuous attribute on same node)

    (*)
    """
    return 0 if math.isnan(G.contattr[attrname][i]) else G.contattr[attrname][i]


def changeo_Oc(attrname, G, A, i):
    """change statistic for continuous exogenous partner attribute o_Oc (outcome
    attribute related to continuous attribute on partner node)

    *--(o)
    """
    delta = 0
    for u in G.neighbourIterator(i):
        delta += 0 if math.isnan(G.contattr[attrname][u]) else G.contattr[attrname][u]
    return delta



def changeoO_Osame(attrname, G, A, i):
    """
    Change statistic for categorical matching exogenous attributes oO_Osame
    (outcome attribtue related to matching categorical exogenous attributes on
    this and partner node)

    {*}--{o}
    """
    delta = 0
    for u in G.neighbourIterator(i):
        if (G.catattr[attrname][u] != NA_VALUE and G.catattr[attrname][i] != NA_VALUE and
            G.catattr[attrname][u] == G.catattr[attrname][i]):
            delta += 1
    return delta


def changeoO_Odiff(attrname, G, A, i):
    """Change statistic for categorical mismatching exogenous attributes
    oO_Odiff (outcome attribtue related to mismatching categorical
    exogenous attributes on this and partner node)

    {*}--<o>

    """
    delta = 0
    for u in G.neighbourIterator(i):
        if (G.catattr[attrname][u] != NA_VALUE and G.catattr[attrname][i] != NA_VALUE and
            G.catattr[attrname][u] != G.catattr[attrname][i]):
            delta += 1
    return delta

def changeSettingHomophily(settingGraph, G, A, i):
    """Change statistic for Setting-Homophily, outcome attribute on two actors
    connected in the setting network.
    
    *...*
    
    (where '...' denotes an edge in the setting network (settingGraph) rather
    than the main network G denoted '--')
    """
    delta = 0
    for u in settingGraph.neighbourIterator(i): #note settingGraph not G
        if A[u] == 1:
            delta += 1
    return delta
