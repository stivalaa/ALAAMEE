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
    return sum([G.isArc(u, i) for u in G.outIterator(i)])


def changeInTwoStar(G, A, i):
    """
    Change statistic for EgoIn2Star (popularity)

    *<--o
     <
      \
       o
    """
    return (G.indegree(i) * (G.indegree(i) - 1))/2.0 if G.indegree(i) > 1 else 0


def changeOutTwoStar(G, A, i):
    """
    Change statistic for EgoOut2Star (activity)

    *-->o
     \
      >
       o
    """
    return (G.outdegree(i) * (G.outdegree(i) - 1))/2.0 if G.outdegree(i) > 1 else 0



def changeContagion(G, A, i):
    """
    change statistic for Contagion (partner attribute)

    *->*
    """
    delta = 0
    delta += sum([(A[u] == 1) for u in G.outIterator(i)])
    delta += sum([(A[u] == 1) for u in G.inIterator(i)])
    return delta


def changeContagionReciprocity(G, A, i):
    """
    change statistic for Contagion Reciprocity (mutual contagion)

    *<->*
    """
    return sum([(G.isArc(u, i) and A[u] == 1) for u in G.outIterator(i)])
