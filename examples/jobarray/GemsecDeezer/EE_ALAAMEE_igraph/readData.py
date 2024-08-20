#!/usr/bin/env python3
#
# File:    run readData.py
# Author:  Alex Stivala
# Created: August 2024
#
"""FUnction to read the GEMSEC Deezer data into an igraph object including
   and network and node attributes.

   This is for demonstrating EE estimation from an igraph object rather than 
   reading the network and data inside ALAAMEE functions.
"""
import igraph
from igraphConvert import fromIgraph

def read_ro_data():
    """
    Read the GEMSEC Deezer Romania data from the ../data directory
    (already converted to network in Pajek format and attributes in
    simple column format by script convertSNAPGemsecDeezerToEEformat.R)
    into an igraph object, convert to ALAAMEE Graph object and return it.
    """
    g = igraph.Graph.Read("../data/deezer_ro_friendship.net", format='pajek')
    g.vs['outcome'] = [bool(int(x)) for x in open('../data/deezer_ro_outcome.txt').readlines()[1:]]
    g.vs['num_genres'] = [float(x) for x in open('../data/deezer_ro_contattr.txt').readlines()[1:]]
    return fromIgraph(g) 
