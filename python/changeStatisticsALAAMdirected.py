#!/usr/bin/env python3
#
# File:    changeStatisticsALAAMdirected.py
# Author:  Alex Stivala
# Created: February 2022
#
"""Functions to compute change statistics for ALAAM on directed
graphs.  Each function takes a Digraph G and outcome vector A and
returns the change statistic for changing outcome of node i to 1.

The attribute statistics take also as their first parameter the name of 
the attribute to use, used as the key in the relevant attribute dictionary
in the Graph object. So that these functions have the same signature as
the structural statistics, use functools.partial() to create a function
with the (G, A, i) signature, e.g. partial(changeo_Oc, "age").
Similarly for the use of the setting network (another fixed graph for
different relationships than the main graph G) the setting-homophily
change statistic is used as e.g. partial(changeSettingHomophily, Gsetting).

The diagrams in the comments describing the change statistics will
follow a convention where a black or solid node, shown as an asterisk
"*" here, denotes an actor with the outcome attribute, while a hollow
or white node, shown as an lowercase "o" here, denotes an actor with
or without the attribute.

See

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  Gallagher, H. C. (2019). Social networks and the willingness to
  communicate: Reciprocity and brokerage. Journal of Language and
  Social Psychology, 38(2), 194-214.

  Parker, A., Pallotti, F., & Lomi, A. (2021). New network models for the
  analysis of social contagion in organizations: an introduction to
  autologistic actor attribute models.
  Organizational Research Methods, 10944281211005167.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.

  Wang, P., Robins, G., & Pattison, P. (2009). PNet: A program for the
  simulation and estimation of exponential random graph
  models. University of Melbourne.

"""
import math

from utils import NA_VALUE
from Digraph import Digraph



def changeSender(G, A, i):
    """
    change statistic for Sender

    *->o
    """
    return G.outdegree(i)


def changeReceiver(G, A, i):
    """
    change statistic for Receiver

    *<-o
    """
    return G.indegree(i)


def changeReciprocity(G, A, i):
    """
    change statistic for Reciprocity

    *<->o
    """
    delta = 0
    for u in G.outIterator(i):
        if G.isArc(u, i):
            delta += 1
    return delta


def changeEgoInTwoStar(G, A, i):
    """
    Change statistic for EgoIn2Star (popularity)

    *<--o
     <
      \
       o
    """
    return (G.indegree(i) * (G.indegree(i) - 1))/2.0 if G.indegree(i) > 1 else 0


def changeEgoOutTwoStar(G, A, i):
    """
    Change statistic for EgoOut2Star (activity)

    *-->o
     \
      >
       o
    """
    return (G.outdegree(i) * (G.outdegree(i) - 1))/2.0 if G.outdegree(i) > 1 else 0


def changeMixedTwoStar(G, A, i):
    """
    Change statistic for Mixed2Star (broker position)

    *<--o
     \
      >
       o
    """
    return (G.indegree(i) * G.outdegree(i) -
            len(set(G.inIterator(i)).intersection(set(G.outIterator(i)))))


def changeMixedTwoStarSource(G, A, i):
    """
    Change statistic for Mixed2StarSource

    o<--*
     \
      >
       o
    """
    delta = 0
    for u in G.outIterator(i):
        delta += G.outdegree(u) - (1 if i in G.outIterator(u) else 0)
    return delta


def changeMixedTwoStarSink(G, A, i):
    """
    Change statistic for Mixed2StarSink

    o<--o
     \
      >
       *
    """
    delta = 0
    for u in G.inIterator(i):
        delta += G.indegree(u) - (1 if i in G.inIterator(u) else 0)
    return delta



def changeContagion(G, A, i):
    """
    change statistic for Contagion (partner attribute)

    *->*
    """
    delta = 0
    for u in G.outIterator(i):
        if A[u] == 1:
            delta += 1
    for u in G.inIterator(i):
        if A[u] == 1:
            delta += 1
    return delta


def changeContagionReciprocity(G, A, i):
    """
    change statistic for Contagion Reciprocity (mutual contagion)

    *<->*
    """
    delta = 0
    for u in G.outIterator(i):
        if A[u] == 1 and G.isArc(u, i):
            delta += 1
    return delta


def changeTransitiveTriangleT1(G, A, i):
    """
    Change statistic for transitive triangle T1

       *
      > \
     /   >
     o-->o

    """
    delta = 0
    for u in G.outIterator(i):
        for v in G.inIterator(u):
            if v != i and G.isArc(v, i):
                delta += 1
    return delta


def changeTransitiveTriangleT3(G, A, i):
    """
    Change statistic for transitive triangle T3 (contagion clustering)

      *
     > \
    /   >
    *-->*

    """
    delta = 0
    for u in G.outIterator(i):
        if A[u] == 1:
            for v in G.outIterator(u):
                if v != i and G.isArc(i, v) and A[v] == 1:
                    delta += 1
    for u in G.outIterator(i):
        if A[u] == 1:
            for v in G.inIterator(u):
                if v != i and G.isArc(v, i) and A[v] == 1:
                    delta +=1
    for u in G.inIterator(i):
        if A[u] == 1:
            for v in G.outIterator(u):
                if v != i and G.isArc(v, i) and A[v] == 1:
                    delta += 1
    return delta


def changeTransitiveTriangleD1(G, A, i):
    """
    Change statistic for transitive triangle D1

      o
     > \
    /   >
    *-->o

    """
    delta = 0
    for u in G.outIterator(i):
        for v in G.outIterator(u):
            if v != i and G.isArc(i, v):
                delta += 1
    return delta


def changeTransitiveTriangleU1(G, A, i):
    """
    Change statistic for transitive triangle U1

      o
     > \
    /   >
    o-->*

    """
    delta = 0
    for u in G.inIterator(i):
        for v in G.outIterator(u):
            if v != i and G.isArc(v, i):
                delta += 1
    return delta


def changeCyclicTriangleC1(G, A, i):
    """
    Change statistic for cyclic triangle C1

       *
      > \
     /   >
     o<--o

    """
    delta = 0
    for u in G.outIterator(i):
        for v in G.outIterator(u):
            if v != i and G.isArc(v, i):
                delta += 1
    return delta


def changeCyclicTriangleC3(G, A, i):
    """
    Change statistic for cyclic triangle C3

       *
      > \
     /   >
     *<--*

    """
    delta = 0
    for u in G.outIterator(i):
        if A[u] == 1:
            for v in G.outIterator(u):
                if v != i and G.isArc(v, i) and A[v] == 1:
                    delta += 1
    return delta


def changeAlterInTwoStar2(G, A, i):
    """
    Change statistic for AlterInTwoStar2
    (structural equivalence between actors with attribute, sharing
    same network partner with arcs directed to them)

    *<--o-->*
    """
    delta = 0
    for u in G.inIterator(i):
        for v in G.outIterator(u):
            if v != i and A[v] == 1:
                delta += 1
    return delta


def changeAlterOutTwoStar2(G, A, i):
    """
    Change statistic for AlterOutTwoStar2
    (structural equivalence between actors with attribute, sharing
    same network partner with arcs directed from them)

    *-->o<--*
    """
    delta = 0
    for u in G.outIterator(i):
        for v in G.inIterator(u):
            if v != i and A[v] == 1:
                delta += 1
    return delta


def changeSenderMatch(attrname, G, A, i):
    """
    Change statistic for categorical matching exogenous attributes
    [attrname]_o->Match
    (outcome attribtue related to matching categorical exogenous attributes on
    this and node receiving tie from this node)

    {*}-->{o}
    """
    delta = 0
    for u in G.outIterator(i):
        if (G.catattr[attrname][u] != NA_VALUE and G.catattr[attrname][i] != NA_VALUE and
            G.catattr[attrname][u] == G.catattr[attrname][i]):
            delta += 1
    return delta

def changeReceiverMatch(attrname, G, A, i):
    """
    Change statistic for categorical matching exogenous attributes
    [attrname]_o<-Match
    (outcome attribtue related to matching categorical exogenous attributes on
    this and node sending tie to this node)

    {*}<--{o}
    """
    delta = 0
    for u in G.inIterator(i):
        if (G.catattr[attrname][u] != NA_VALUE and G.catattr[attrname][i] != NA_VALUE and
            G.catattr[attrname][u] == G.catattr[attrname][i]):
            delta += 1
    return delta

def changeReciprocityMatch(attrname, G, A, i):
    """
    Change statistic for categorical matching exogenous attributes
    [attrname]_o<->Match
    (outcome attribtue related to matching categorical exogenous attributes on
    this and node with mutual (reciprocated) ties with this node)

    {*}<->{o}
    """
    delta = 0
    for u in G.outIterator(i):
        if (G.catattr[attrname][u] != NA_VALUE and
            G.catattr[attrname][i] != NA_VALUE and
            G.catattr[attrname][u] == G.catattr[attrname][i] and
            G.isArc(u, i)):
            delta += 1
    return delta

def changeSenderMismatch(attrname, G, A, i):
    """Change statistic for categorical mismatching exogenous
    attributes [attrname]_o->Mismatch (outcome attribtue related to
    mismatching categorical exogenous attributes on this and node
    receiving tie from this node)

    {*}--><o>

    """
    delta = 0
    for u in G.outIterator(i):
        if (G.catattr[attrname][u] != NA_VALUE and G.catattr[attrname][i] != NA_VALUE and
            G.catattr[attrname][u] != G.catattr[attrname][i]):
            delta += 1
    return delta

def changeReceiverMismatch(attrname, G, A, i):
    """Change statistic for categorical mismatching exogenous
    attributes [attrname]_o<-Mismatch (outcome attribtue related to
    mismatching categorical exogenous attributes on this and node
    sending tie to this node)

    {*}<--<o>

    """
    delta = 0
    for u in G.inIterator(i):
        if (G.catattr[attrname][u] != NA_VALUE and G.catattr[attrname][i] != NA_VALUE and
            G.catattr[attrname][u] != G.catattr[attrname][i]):
            delta += 1
    return delta

def changeReciprocityMismatch(attrname, G, A, i):
    """Change statistic for categorical mismatching exogenous
    attributes [attrname]_o<->Mismatch (outcome attribtue related to
    mismatching categorical exogenous attributes on this and node with
    mutual (reciprocated) ties with this node)

    {*}<-><o>

    """
    delta = 0
    for u in G.outIterator(i):
        if (G.catattr[attrname][u] != NA_VALUE and
            G.catattr[attrname][i] != NA_VALUE and
            G.catattr[attrname][u] != G.catattr[attrname][i] and
            G.isArc(u, i)):
            delta += 1
    return delta


def changeGWSender(G, A, i):
    """Change statistic for Geometrically Weighted Sender.

        >o
      /
     *-->o
      \ :
       >o


    This is an ALAAM analogue of the geometrically weighted out-degree
    statistic defined by Equation (31) in:

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

    The purpose of this statistic is to try to avoid problems with
    near-degeneracy when using the Activity, Two-Star, Three-Star,
    etc. parameters, by instead using this parameter to model
    alternating out-k-stars or alternatively as in this parameterization,
    geometrically weighted out-degree distribution.

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
    contribution of the single term for i in Equation (31) of Snijders
    et al. (2007), which is a sum over all nodes.

    """
    # Note lambda_s = exp(alpha)/(exp(alpha)-1) [p. 113 Snjders et al. 2006]
    # and 1/lambda_s = exp(-theta_s) = 1 - exp(-alpha) [p. 222 Hunter 2007]
    lambda_s = 2.0 # TODO make it a function parameter
    #theta_s = -math.log(1/lambda_s)
    alpha = -math.log(1 - 1/lambda_s)

    return math.exp(-alpha * G.outdegree(i))


def changeGWReceiver(G, A, i):
    """Change statistic for Geometrically Weighted Receiver.
    
          o
        /
      <
     *<--o
      <  :
        \
         o


    This is an ALAAM analogue of the geometrically weighted in-degree
    statistic defined by Equation (32) in:

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

    The purpose of this statistic is to try to avoid problems with
    near-degeneracy when using the Activity, Two-Star, Three-Star,
    etc. parameters, by instead using this parameter to model
    alternating in-k-stars or alternatively as in this parameterization,
    geometrically weighted in-degree distribution.

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
    contribution of the single term for i in Equation (32) of Snijders
    et al. (2007), which is a sum over all nodes.

    """
    # Note lambda_s = exp(alpha)/(exp(alpha)-1) [p. 113 Snjders et al. 2006]
    # and 1/lambda_s = exp(-theta_s) = 1 - exp(-alpha) [p. 222 Hunter 2007]
    lambda_s = 2.0 # TODO make it a function parameter
    #theta_s = -math.log(1/lambda_s)
    alpha = -math.log(1 - 1/lambda_s)

    return math.exp(-alpha * G.indegree(i))


# ================== old versions for regression testing ======================

def changeContagion_OLD(G, A, i):
    """
    change statistic for Contagion (partner attribute)

    *->*

    More elegant version using list comprehensions instead of loops, but
    unfortunately turns out to be slower than loop version.
    """
    delta = 0
    delta += sum([(A[u] == 1) for u in G.outIterator(i)])
    delta += sum([(A[u] == 1) for u in G.inIterator(i)])
    return delta

def changeContagion_GENCOMP(G, A, i):
    """
    change statistic for Contagion (partner attribute)

    *->*

    More elegant version using generator comprehensions instead of loops,
    or list comprehensions (which are slower than loops for this). 
    Unfortunately generator comprehension is just the same speed as list
    comprehension here (does sum end up converting the iterator to a list?). 
    Or not(?): https://stackoverflow.com/questions/62975325/why-is-summing-list-comprehension-faster-than-generator-expression
    """
    delta = 0
    delta += sum((A[u] == 1) for u in G.outIterator(i))
    delta += sum((A[u] == 1) for u in G.inIterator(i))
    return delta

def changeContagionReciprocity_OLD(G, A, i):
    """
    change statistic for Contagion Reciprocity (mutual contagion)

    *<->*

    More elegant version using list comprehensions instead of loops, but
    unfortunately turns out to be slower than loop version.
    """
    return sum([(G.isArc(u, i) and A[u] == 1) for u in G.outIterator(i)])

def changeReciprocity_OLD(G, A, i):
    """
    change statistic for Reciprocity

    *<->o

    More elegant version using list comprehensions instead of loops, but
    unfortunately turns out to be slower than loop version.
    """
    return sum([G.isArc(u, i) for u in G.outIterator(i)])
