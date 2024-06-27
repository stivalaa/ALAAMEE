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
import numpy
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
        suffix = ".".join(["matrix" if isinstance(x, numpy.ndarray)
                           else str(x) for x in param_func.args])
    else:
        funcname = param_func.__name__
        suffix = None

    label = funcname[len(prefix):] if funcname.startswith(prefix) else funcname
    if suffix is not None:
        label += "." + suffix
    return label


def is_same_changestat(func1, func2):
    """Return True if two change statistic funcions are the same, else False.
    This is needed for example when we use functools.partial(), as two of
    these will be different function addresses and hence not equal, even
    if they have the same parameter.

    Parameters:
        func1 - change statistic function
        func2 - another change setatistic function

    Return value:
        True if func1 and func2 are the same change statistic function else
        False
    """
    # We will take advantage of the param_func_to_label() function
    # to just check if they have the same string representation.
    return param_func_to_label(func1) == param_func_to_label(func2)


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

    Note the PNet manual (Wang et al., 2019) is apparently wrong
    (or at least does not agree with what IPNet implemented) here
    for "Setting-Homophily" which is dnoted as having both the red
    and black (setting and networ) edges [p. 42]: in fact in IPNet
    (and hence here) only the setting edge is required, the IPNet code
    does not test for a network edge at all.
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




def changeGeographicHomophily(distmatrix, G, A, i):
    """Change statistic for GeographicHomophily, outcome attribute on
    two actors related to the distance betwen them
    
    *...*

    (where '...' denotes the distance as specified in distmatrix).
    The distance matrix distmatrix is an NxN numpy matrix (where N is
    the number of nodes in G) where distmatrix[i,j] is the distance
    beetween nodes i and j.

    In the PNet manual (Wang et al., 2009) this is called
    "Geographic-Homophily" (p. 42), and in Daraganova & Robins (2013)
    is referred to as "Attribute proximity [geographic homophily]"
    "represented as dyadic covariate of logarithm of distance" (p. 245).
    (Note we are not using logarithm here, just distance as is).
    This is explicitly noted as accounting for geographic distance,
    "regardless of whether these people are friends." (Daraganova & 
    Robins 2013, p. 245).

    TODO: Note this implementation is not scalable to large networks, as the
    distance matrix is NxN. For large networks, need to implement a version
    that instead of a matrix calls a function to find the distance between
    two nodes. However, even then, this change statistic involves
    iterating over all nodes, rather than just neighbour nodes, and so
    is not scalable.

    """
    delta = 0
    for u in G.nodeIterator():
        if u != i and A[u] == 1:
            delta += distmatrix[i, u]
    return delta


def changeContagionDist(distmatrix, G, A, i):
    """Change statistic for ContagionDist, outcome attribute on two
    directly connected actors related to the distance betwen them
    
    *...*
     ---
    
    (where '...' denotes the distance as specified in distmatrix and
    --- the network in G). The distance matrix distmatrix is an NxN
    numpy matrix (where N is the number of nodes in G) where
    distmatrix[i,j] is the distance beetween nodes i and j.

    In the PNet manual (Wang et al., 2009) this is called
    "Contagion-among-partners" (p. 42).

    TODO: Note this implementation is not scalable to large networks, as the
    distance matrix is NxN. For large networks, need to implement a version
    that instead of a matrix calls a function to find the distance between
    two nodes.

    """
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] == 1:
            delta += distmatrix[i, u]
    return delta



def changeSamePartnerActivityTwoPath(attrname, G, A, i):
    """Change statistic for SamePartnerActivityTwoPath,
    two-path from a node with outcome attribute where both ends
    of two-path have same value of cateogorical attribute attrname.

    {*}--o--{o}

    This is like changePartnerActivityTwoPath (change statistic for
    partner activity actor two-path (Alter-2Star1)), but with the
    additional requirement that the two nodes on the ends of the two-path
    have the same value of the supplied categorical attribute.

    """
    delta = 0
    for u in G.neighbourIterator(i):
        for v in G.neighbourIterator(u):
            if (v != i and
                G.catattr[attrname][i] != NA_VALUE and
                G.catattr[attrname][v] != NA_VALUE and
                G.catattr[attrname][i] == G.catattr[attrname][v]):
                delta += 1
    return delta


def changeDiffPartnerActivityTwoPath(attrname, G, A, i):
    """Change statistic for DiffPartnerActivityTwoPath,
    two-path from a node with outcome attribute where ends
    of two-path have different values of cateogorical attribute attrname.

    {*}--o--<o>

    This is like changePartnerActivityTwoPath (change statistic for
    partner activity actor two-path (Alter-2Star1)), but with the
    additional requirement that the two nodes on the ends of the two-path
    have different values of the supplied categorical attribute.

    """
    delta = 0
    for u in G.neighbourIterator(i):
        for v in G.neighbourIterator(u):
            if (v != i and
                G.catattr[attrname][i] != NA_VALUE and
                G.catattr[attrname][v] != NA_VALUE and
                G.catattr[attrname][i] != G.catattr[attrname][v]):
                delta += 1
    return delta


def changeSameIndirectPartnerAttribute(attrname, G, A, i):
    """Change statistic for SameIndirectPartnerAttribute,
    structural equivalence between actors with attribute (two-path
    equivalence) which also have the same value of the supplied
    categorical attribute attrname.

    {*}--o--{*}

    This is like changeIndrectPartnerAttribute (indirect partner
    attribute (Alter-2Star2); structural equivalence between actors
    with attribute (two-path equivalence), but with the additional
    requirement that the two structurally equivalent nodes also have
    the same value of the categorical attribute attrname.

    """
    delta = 0
    for u in G.neighbourIterator(i):
        for v in G.neighbourIterator(u):
            if (v != i and A[v] == 1 and
                G.catattr[attrname][i] != NA_VALUE and
                G.catattr[attrname][v] != NA_VALUE and
                G.catattr[attrname][i] == G.catattr[attrname][v]):
                delta += 1
    return delta


def changeDiffIndirectPartnerAttribute(attrname, G, A, i):
    """Change statistic for DiffIndirectPartnerAttribute,
    structural equivalence between actors with attribute (two-path
    equivalence) which also have different values of the supplied
    categorical attribute attrname.

    {*}--o--<*>

    This is like changeIndrectPartnerAttribute (indirect partner
    attribute (Alter-2Star2); structural equivalence between actors
    with attribute (two-path equivalence), but with the additional
    requirement that the two structurally equivalent nodes also have
    the same value of the categorical attribute attrname.

    """
    delta = 0
    for u in G.neighbourIterator(i):
        for v in G.neighbourIterator(u):
            if (v != i and A[v] == 1 and
                G.catattr[attrname][i] != NA_VALUE and
                G.catattr[attrname][v] != NA_VALUE and
                G.catattr[attrname][i] != G.catattr[attrname][v]):
                delta += 1
    return delta


def changeAlterBinaryTwoStar1(attrname, G, A, i):
    """Change statistic for AlterBinaryTwoStar1, tendency of an actor
    with the attribute to have a tie to another actor, which has the
    binary attribute attrname, with a tie to a third actor.

    *--[o]--o

    Like changePartnerActivityTwoPath (change statistic for partner
    activity actor two-path (Alter-2Star1)), but with the added
    requirement that the binary attribute for the central node in the
    two-path is true.

    """
    return sum([G.degree(v) - 1 for v in G.neighbourIterator(i)
                if G.binattr[attrname][v] != NA_VALUE and
                G.binattr[attrname][v]])


def changeAlterBinaryTwoStar2(attrname, G, A, i):
    """Change statistic for AlterBinaryTwoStar2, structural
    equivalence of actors with the attribute (two-path equivalence, or
    tendency of actors with the attribute to have the same network
    partner in common), when that common network partner has the binary
    attribute attrname.
    
    *--[o]--*

    Like changeIndirectedPartnerAttribute (change statistic for
    indirect partner attribute (Alter-2Star2); structural equivalence
    between actors with attribute (two-path equivalence)), but with the
    added requirement that the binary attribute for the central node in the
    two-path is true.

    """
    delta = 0
    for u in G.neighbourIterator(i):
        if (G.binattr[attrname][u] != NA_VALUE and G.binattr[attrname][u]):
            for v in G.neighbourIterator(u):
                if v != i and A[v] == 1:
                    delta += 1
    return delta


# ======================= experimental statistics ============================

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

    Note that this statistic may not actually be useful (in particular
    difficult or impossible to interpret its corresponding parameter)
    as this change statistic can be negative or positive, depending
    on the number of neighbour nodes of i with the outcome variable,
    and the number of neighbour nodes of those neigbbours with the outcome
    varaible.

    Doing simulation experiments, if we vary GWContagion (keeping other
    paramters fixed), and plot the value of the Contagion statistic against
    the value of the GWContagion parameter,
    then it can be increasing, or decreasing, depending on the network.

    Implemented with only (ugly and more code) loops, as it is faster
    than more elegant implementation using list comprehensions.

    """
    delta = 0
    diplus = 0
    for j in G.neighbourIterator(i):
        djplus = 0
        if A[j] == 1:
            diplus += 1
            for v in G.neighbourIterator(j):
                if A[v] == 1:
                    djplus += 1
            delta += (math.exp(-alpha * (djplus + 1)) -
                      math.exp(-alpha * djplus))
    delta += math.exp(-alpha * diplus)
    return delta


def changeLogContagion(G, A, i):
    """Change statistic for Logarithmic Contagion.


       *
      /
     *--*
      \ :
       *


    Implemented with only (ugly and more code) loops, as it is faster
    than more elegant implementation using list comprehensions.

    """
    ## Note adding one to degree so never have log(0)
    delta = 0
    diplus = 0
    for j in G.neighbourIterator(i):
        djplus = 0
        if A[j] == 1:
            diplus += 1
            for v in G.neighbourIterator(j):
                if A[v] == 1:
                    djplus += 1
            # delta += (math.log(djplus + 2) -
            #           math.log(djplus + 1))
            delta += math.log((djplus + 2) / (djplus + 1))
    delta += math.log(diplus + 1)
    return delta


def changePowerContagion(beta, G, A, i):
    """Change statistic for Power Contagion


       *
      /
     *--*
      \ :
       *

    beta > 0 specifies the power 1/beta that the contagion statisic
    is raised to.

    This is based on the idea from Wilson et al. (2017) described
    in Blackburn & Handockc (2022) of raising network statistics
    to a positive power less than one. So e.g. would hvae beta = 2
    for square root.

    Implemented with only (ugly and more code) loops, as it is faster
    than more elegant implementation using list comprehensions.

    References:

    Blackburn, B., & Handcock, M. S. (2023). Practical network
    modeling via tapered exponential-family random graph models.
    Journal of Computational and Graphical Statistics, 32(2), 388-401.

    Wilson, J. D., Denny, M. J., Bhamidi, S., Cranmer, S. J., &
    Desmarais, B. A. (2017). Stochastic weighted graphs: Flexible
    model specification and simulation. Social Networks, 49, 37-47.

    """
    delta = 0
    diplus = 0
    for j in G.neighbourIterator(i):
        djplus = 0
        if A[j] == 1:
            diplus += 1
            for v in G.neighbourIterator(j):
                if A[v] == 1:
                    djplus += 1
            delta += (math.pow(djplus + 1, 1/beta) -
                      math.pow(djplus, 1/beta))
    delta += math.pow(diplus, 1/beta)
    return delta



# ================== old versions for regression testing ======================

def changePartnerPartnerAttribute_OLD(G, A, i):
    """
    Change statistic for partner-partner-attribute (partner-resource)

    *--*--*
    """
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] == 1:
            # this is inefficient, iterating over all nodes
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


def changeContagion_LISTCOMP(G, A, i):
    """
    change statistic for Contagion (partner attribute)

    *--*

    More elegant version using list comprehensions not loops, 
    unfortunately this is slower than loop version.
    """
    return sum([(A[u] == 1) for u in G.neighbourIterator(i)])

def changeContagion_GENEXP(G, A, i):
    """
    change statistic for Contagion (partner attribute)

    *--*

    More elegant version using generator expression not loops, 
    unfortunately this is slower than loop version.
    """
    return sum((A[u] == 1) for u in G.neighbourIterator(i))


def changeGWContagion_LISTCOMP(alpha, G, A, i):
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

    Note that this statistic may not actually be useful (in particular
    difficult or impossible to interpret its corresponding parameter)
    as this change statistic can be negative or positive, depending
    on the number of neighbour nodes of i with the outcome variable,
    and the number of neighbour nodes of those neigbbours with the outcome
    varaible.

    Doing simulation experiments, if we vary GWContagion (keeping other
    paramters fixed), and plot the value of the Contagion statistic against
    the value of the GWContagion parameter,
    then it can be increasing, or decreasing, depending on the network.

    This version uses list comprehensions meaning there is less code
    and it is more elegant and readable, but unfortunately slower.
    """
    delta = math.exp(-alpha * sum([(A[u] == 1)
                                   for u in G.neighbourIterator(i)]))
    for j in G.neighbourIterator(i):
        if A[j] == 1:
            djplus = sum([(A[u] == 1) for u in G.neighbourIterator(j)])
            delta += (math.exp(-alpha * (djplus + 1)) -
                      math.exp(-alpha * djplus))
    return delta
