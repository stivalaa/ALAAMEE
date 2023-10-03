#!/usr/bin/env python3
#
# File:    changeStatisticsALAAM.py
# Author:  Alex Stivala
# Created: February 2020
#
"""Functions to compute change statistics for ALAAM. Each function
takes a Graph G and outcome vector A and returns the change statistic
for changing outcome of node i to 1.

The attribute statistics take also as their first parameter the name of 
the attribute to use, used as the key in the relevant attribute dictionary
in the Graph object. So that these functions have the same signature as
the structural statistics, use functools.partial() to create a function
with the (G, A, i) signature, e.g. partial(changeo_Oc, "age").
Similarly for the use of the setting network (another fixed graph for
different relationships than the main graph G) the setting-homophily
change statistic is used as e.g. partial(changeSettingHomophily, Gsetting).
The same technique is used for the geometrically weighted statistics
e.g. partial(changeGWActivity, math.log(2))

Most of the change statistics here are documented in Daraganova & Robins
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

  Stivala, A. (2023). Overcoming near-degeneracy in the autologistic 
  actor attribute model. arXiv preprint arXiv:2309.07338.
  https://arxiv.org/abs/2309.07338

  Stivala, A., Wang, P., & Lomi, A. (2023). ALAAMEE: Open-source
  software for fitting autologistic actor attribute
  models. Unpublished manuscript.

  Wang, P., Robins, G., & Pattison, P. (2009). PNet: A program for the
  simulation and estimation of exponential random graph
  models. University of Melbourne.

"""

import math
import functools

from utils import NA_VALUE
from Graph import Graph



def param_func_to_label(param_func):
    """Return string label for a change statistic function, for
   use in automatically generating the labels for the param_func_list
   list of functions in the estimation functions like
   estimateALAAMEE.run_on_network_attr()

    Parameters:
        param_func - change statistic function from changeStatisticsALAAM.py
                     etc. e.g changeActivity

    Return value:
        label for parameter corresponding to the change statistic.

    The name of the function is obtained using its __name__ attribute,
    and the "change" at the front removed. 
    For functions created with functools.partial(), e.g.
    partial(changeo_Oc, "age"), we get the original function and paramters via
    the func and args attributes, and the parameter is appended to the function
    name after a period, to get e.g. "changeeo_Oc.age"
    """
    prefix = "change"
    if isinstance(param_func, functools.partial):
        funcname = param_func.func.__name__
        suffix = ".".join([str(x) for x in param_func.args])
    else:
        funcname = param_func.__name__
        suffix = None

    label = funcname[len(prefix):] if funcname.startswith(prefix) else funcname
    if suffix is not None:
        label += "." + suffix
    return label



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
    Change statistic for partner activity actor two-path (Alter-2Star1)

    *--o--o
    """
    return sum([G.degree(v) - 1 for v in G.neighbourIterator(i)])
    

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
    Change statistic for indirect partner attribute (Alter-2Star2);
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
    

def changePartnerPartnerAttribute(G, A, i):
    """
    Change statistic for partner-partner-attribute (partner-resource)

    *--*--*
    """
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] == 1:
            for v in G.neighbourIterator(u):
                if A[v] == 1:
                    delta += 2
            for v in G.neighbourIterator(i):
                if A[v] == 1 and v != u:
                    delta += 1
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
        delta += 0 if G.binattr[attrname][u] == NA_VALUE else G.binattr[attrname][u]
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


def changeoO_OsameContagion(attrname, G, A, i):
    """
    Change statistic for categorical matching exogenous attributes oO_Osame
    contagion (outcome attribtue on both nodes with matching categorical
    exogenous attributes)

    {*}--{*}
    """
    delta = 0
    for u in G.neighbourIterator(i):
        if (G.catattr[attrname][u] != NA_VALUE and G.catattr[attrname][i] != NA_VALUE and
            G.catattr[attrname][u] == G.catattr[attrname][i] and
            A[u] == 1):
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


def changeGWActivity(alpha, G, A, i):
    """Change statistic for Geometrically Weighted Activity.

       o
      /
     *--o
      \ :
       o


    This is an ALAAM analogue of the geometrically weighted degree
    statistic defined by Equation (11) in:

    Snijders, T. A., Pattison, P. E., Robins, G. L., & Handcock,
    M. S. (2006). New specifications for exponential random graph
    models. Sociological methodology, 36(1), 99-153.

    See also Section 3 (pp. 219-222) in:

    Hunter, D. R. (2007). Curved exponential family models for social
    networks. Social networks, 29(2), 216-230.

    and the Remark on p. 222 of Hunter (2007) relating the GWD
    statistic defined there to that defined in Snijders et al. (2006),
    and both papers for the relationships between gwdegree and the
    alternating k-star statistic.

    alpha > 0 is the decay parameter controlling the geometric rate of
    decrease in the weights. For large alpha, the contribution of
    positive outcomes on higher degree nodes is decreased. As alpha goes
    to 0, increasing weight is placed on outcome vectors with positive
    outcome on high degree nodes.  See Sjniders et a. (2006) p. 112.

    Note lambda_s = exp(alpha)/(exp(alpha)-1) [p. 113 Snjders et al. 2006]
    and 1/lambda_s = exp(-theta_s) = 1 - exp(-alpha) [p. 222 Hunter 2007]
    theta_s = -log(1/lambda_s)
    alpha = -log(1 - 1/lambda_s)
    So for the "traditional" value of lambda = 2 we have
    alpha = -log(1 - 1/2) = -log(1/2) = log(2) =appox 0.69


    The purpose of this statistic is to try to avoid problems with
    near-degeneracy when using the Activity, Two-Star, Three-Star,
    etc. parameters, by instead using this parameter to model
    alternating k-stars or alternatively as in this parameterization,
    geometrically weighted degree distribution.

    Note that the change statistic for ERGM (described in those
    papers) is not the change statistic here for ALAAM. In ERGM,
    modeling the network (stars or degree distribution here) the
    change statistic is for adding an edge, and so involves counting
    the additional number of stars created by adding an extra edge.
    However for ALAAM, the network is fixed, and the change statistic
    is for switching the outcome of node i from 0 to 1, and hence the
    number of stars (or activity degree) at the node is 0 before the
    the switch, and hence the change statistic is just related to the
    number of stars at the node i. And hence this is just the
    contribution of the single term for i in Equation (11) of Snijders
    et al. (2007), which is a sum over all nodes.

    Reference:

     Stivala, A. (2023). Overcoming near-degeneracy in the autologistic 
     actor attribute model. arXiv preprint arXiv:2309.07338.
     https://arxiv.org/abs/2309.07338

    """
    return math.exp(-alpha * G.degree(i))


def changeGWContagion(alpha, G, A, i):
    """Change statistic for Geometrically Weighted Contagion.

       *
      /
     *--*
      \ :
       *


    This is like GWActivity, but with the outcome on all the Alter
    nodes as well as Ego. The idea is to use this rather than
    Contagion to test for Alters and Ego both having outcome, but with
    geometic decay to help prevent near-degeneracy problems, just as
    GWActivity does when used instead of Activity (and TwoStar, etc.)

    """
    return math.exp(-alpha * changeContagion(G, A, i))


 
# ================== old versions for regression testing ======================

def changePartnerPartnerAttribute_OLD(G, A, i):
    """
    Change statistic for partner-partner-attribute (partner-resource)

    *--*--*
    """
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] == 1:
            # FIXME this is inefficient, iterating over all nodes
            for v in range(G.numNodes()):
                if v == i or v == u:
                    continue
                if A[v] == 1:
                    if G.isEdge(u, v):
                        delta += 2
                    if G.isEdge(i, v):
                        delta += 1
    return delta


def changeTriangleT1_OLD(G, A, i):
    """
    Change statistic for actor triangle (T1)

      o
     / \
    *---o

    More elegant version using list comprehensions not loops, 
    unfortunately this is slower than loop version.
    """
    return (0 if G.degree(i) < 2 else
            sum([int(G.isEdge(i, v))
                 for u in G.neighbourIterator(i)
                 for v in G.neighbourIterator(u)]) // 2)


def changeContagion_SLOWER(G, A, i):
    """
    change statistic for Contagion (partner attribute)

    *--*

    More elegant version using list comprehensions not loops, 
    unfortunately this is slower than loop version.
    """
    return sum([(A[u] == 1) for u in G.neighbourIterator(i)])

