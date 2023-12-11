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
The same technique is used for the geometrically weighted statistics
e.g. partial(changeGWSender, math.log(2))

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
    Change statistic for EgoIn2Star

    *<--o
     <
      \
       o
    """
    return (G.indegree(i) * (G.indegree(i) - 1))/2.0 if G.indegree(i) > 1 else 0


def changeEgoInThreeStar(G, A, i):
    """
    Change statistic for EgoIn3Star

        o
       /
     <
    *<--o
     ^
      \
       o
    """
    return ( G.indegree(i) * (G.indegree(i) - 1) * (G.indegree(i) - 2) / 6.0
             if G.indegree(i) > 2 else 0 )

def changeEgoOutTwoStar(G, A, i):
    """
    Change statistic for EgoOut2Star

    *-->o
     \
      >
       o
    """
    return (G.outdegree(i) * (G.outdegree(i) - 1))/2.0 if G.outdegree(i) > 1 else 0

def changeEgoOutThreeStar(G, A, i):
    """
    Change statistic for EgoOut3Star

      o
      ^
     /
    *-->o
     \
      >
       o
    """
    return ( G.outdegree(i) * (G.outdegree(i) - 1) * (G.outdegree(i) - 2) / 6.0
             if G.outdegree(i) > 2 else 0 )

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


def changeGWSender(alpha, G, A, i):
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

    Reference:

      Stivala, A. (2023). Overcoming near-degeneracy in the autologistic 
      actor attribute model. arXiv preprint arXiv:2309.07338.
      https://arxiv.org/abs/2309.07338
    """
    return math.exp(-alpha * G.outdegree(i))


def changeGWReceiver(alpha, G, A, i):
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

    alpha > 0 is the decay parameter controlling the geometric rate of
    decrease in the rates. For large alpha, the contribution of
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

    Reference:

      Stivala, A. (2023). Overcoming near-degeneracy in the autologistic 
      actor attribute model. arXiv preprint arXiv:2309.07338.
      https://arxiv.org/abs/2309.07338

    """
    return math.exp(-alpha * G.indegree(i))


# ======================= experimental statistics ============================

def changeGWContagion(alpha, G, A, i):
    """Change statistic for Geometrically Weighted Contagion.

        >*
      /
     *-->*
      \ :
       >*

          *
        /
      <
     *<--*
      <  :
        \
         *

    This is a geometrically weighted version of changeContagion.
    The idea is to use this rather than
    Contagion to test for Alters and Ego both having outcome, but with
    geometic decay to help prevent near-degeneracy problems, just as
    GWSender and GWReceiver does when used instead of Sender and Receiver
    (and EgoInTwoStar, EgoOutTwoStar, etc.)

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
    for j in G.outIterator(i):
        djplus = 0
        if A[j] == 1:
            diplus += 1
            for v in G.inIterator(j):
                if A[v] == 1:
                    djplus += 1
            delta += (math.exp(-alpha * (djplus + 1)) -
                      math.exp(-alpha * djplus))
    delta += math.exp(-alpha * diplus)

    diplus = 0
    for j in G.inIterator(i):
        djplus = 0
        if A[j] == 1:
            diplus += 1
            for v in G.outIterator(j):
                if A[v] == 1:
                    djplus += 1
            delta += (math.exp(-alpha * (djplus + 1)) -
                      math.exp(-alpha * djplus))
    delta += math.exp(-alpha * diplus)
            
    return delta


def changeLogContagion(G, A, i):
    """Change statistic for Log Contagion.

        >*
      /
     *-->*
      \ :
       >*

          *
        /
      <
     *<--*
      <  :
        \
         *


    Implemented with only (ugly and more code) loops, as it is faster
    than more elegant implementation using list comprehensions.

    """
    ## Note adding one to degree so never have log(0)
    delta = 0
    diplus = 0
    for j in G.outIterator(i):
        djplus = 0
        if A[j] == 1:
            diplus += 1
            for v in G.inIterator(j):
                if A[v] == 1:
                    djplus += 1
            # delta += (math.log(djplus + 2) -
            #           math.log(djplus + 1))
            delta += math.log((djplus + 2) / (djplus + 1))
    delta += math.log(diplus + 1)

    diplus = 0
    for j in G.inIterator(i):
        djplus = 0
        if A[j] == 1:
            diplus += 1
            for v in G.outIterator(j):
                if A[v] == 1:
                    djplus += 1
            # delta += (math.log(djplus + 2) -
            #           math.log(djplus + 1))
            delta += math.log((djplus + 2) / (djplus + 1))
    delta += math.log(diplus + 1)

    return delta


def changePowerContagion(beta, G, A, i):
    """Change statistic for Power Contagion.

        >*
      /
     *-->*
      \ :
       >*

          *
        /
      <
     *<--*
      <  :
        \
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


    Implemented with only (ugly and more code) loops, as it is faster
    than more elegant implementation using list comprehensions.

    """
    delta = 0
    diplus = 0
    for j in G.outIterator(i):
        djplus = 0
        if A[j] == 1:
            diplus += 1
            for v in G.inIterator(j):
                if A[v] == 1:
                    djplus += 1
            delta += (math.pow(djplus + 1, 1/beta) -
                      math.pow(djplus, 1/beta))
    delta += math.pow(diplus, 1/beta)

    diplus = 0
    for j in G.inIterator(i):
        djplus = 0
        if A[j] == 1:
            diplus += 1
            for v in G.outIterator(j):
                if A[v] == 1:
                    djplus += 1
            delta += (math.pow(djplus + 1, 1/beta) -
                      math.pow(djplus, 1/beta))
    delta += math.pow(diplus, 1/beta)

    return delta

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

def changeGWContagion_LISTCOMP(alpha, G, A, i):
    """Change statistic for Geometrically Weighted Contagion.

        >*
      /
     *-->*
      \ :
       >*

          *
        /
      <
     *<--*
      <  :
        \
         *

    This is a geometrically weighted version of changeContagion.
    The idea is to use this rather than
    Contagion to test for Alters and Ego both having outcome, but with
    geometic decay to help prevent near-degeneracy problems, just as
    GWSender and GWReceiver does when used instead of Sender and Receiver
    (and EgoInTwoStar, EgoOutTwoStar, etc.)

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
                                   for u in G.outIterator(i)]))
    for j in G.outIterator(i):
        if A[j] == 1:
            djplus = sum([(A[u] == 1) for u in G.inIterator(j)])
            delta += (math.exp(-alpha * (djplus + 1)) -
                      math.exp(-alpha * djplus))

    delta += math.exp(-alpha * sum([(A[u] == 1)
                                   for u in G.inIterator(i)]))
    for j in G.inIterator(i):
        if A[j] == 1:
            djplus = sum([(A[u] == 1) for u in G.outIterator(j)])
            delta += (math.exp(-alpha * (djplus + 1)) -
                      math.exp(-alpha * djplus))
            
    return delta
