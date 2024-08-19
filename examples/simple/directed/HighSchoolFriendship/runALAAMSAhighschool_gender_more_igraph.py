#!/usr/bin/env python3
#
# File:    runALAAMSAhighschool_gender_more_igraph.py
# Author:  Alex Stivala
# Created: August 2024
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the SocioPatterns high school frienship network
 with gender as "outcome" variable.

 See ../../../data/directed/HighSchoolFriendship/README.txt 
 for more details.

 This version uses python-igraph to read the data from the original format
 and convert it directly in this script to the format for ALAAMEE,
 rather than using the data already converted wih the
 convert_highschoolfriendship_directed_network_to_pajek_ALAAMEE_format.R
 script (which in turn uses load_highschoolfriendship_network.R using
 R/igraph). 
"""
import os
import gzip
from functools import partial
import igraph
from igraphConvert import fromIgraph
import estimateALAAMSA
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity, param_func_to_label

from gof_stats import gof_funcs


#
# Read edge list (two column, space delimited, no header) from compressed
# file, convert to list of tuples, and build igraph graph object from it
#
datadir = os.path.join("..", "..", "..", "data", "directed", "HighSchoolFriendship")
edgelist_text = gzip.open(os.path.join(datadir,"Friendship-network_data_2013.csv.gz"), mode="rt").readlines()
edgelist_tuples = [tuple(s.split()) for s in edgelist_text]
Gigraph = igraph.Graph.TupleList(edgelist_tuples, directed = True)


#
# Read the node attributes and add to igraph object
#

node_attrs_filename = os.path.join(datadir, 'metadata_2013.txt')

# metadata_2013.txt
# "-Finally the metadata file contains a tab-separated list in which each line of the form “i Ci Gi” gives class Ci and gender Gi of the person having ID i."

# Note in the following,
#  map(list, zip(*[row.split() for row in open(filename).readlines()]))
# reads the data and transposes it so we have a list of columns
# not a list of rows, which then makes it easy to convert to
# the dict where key is column header and value is list of values
# https://stackoverflow.com/questions/6473679/transpose-list-of-lists#

attr_names = ['id', 'class', 'sex']
attr_data = list(map(list, list(zip(*[row.split() for row in open(node_attrs_filename).readlines()]))))
assert(len(attr_data) == len(attr_names))
attr_dict = dict([(attr_names[i], attr_data[i]) for i in range(len(attr_names))])
for v in Gigraph.vs:
    for aname in ['class', 'sex']:
        v[aname] = attr_dict[aname][attr_dict['id'].index(v['name'])]


# Replace "Unknown" values with "NA"
Gigraph.vs["sex"] = [sex if sex in ["F", "M"] else "NA" for sex in Gigraph.vs["sex"]]

#
# Convert sex to binary attribute male with True for male and False for female
# (also for the single "Unknown")
#

Gigraph.vs["male"] = [True if sex == "M" else False for sex in Gigraph.vs["sex"]]


#
# Convert to directed graph (Digraph) object for ALAAMEE
#

G = fromIgraph(Gigraph)


#
# Estimate the model specfieidy by param_func_list with
# stochastic approximation algorithm
#
param_func_list =  [changeDensity, changeSender, changeReceiver, changeEgoInTwoStar, changeEgoInThreeStar, changeEgoOutTwoStar, changeEgoOutThreeStar, changeContagion, changeReciprocity, changeContagionReciprocity, changeMixedTwoStarSource, changeMixedTwoStarSink, changeTransitiveTriangleT1, changeTransitiveTriangleT3, partial(changeSenderMatch, "class"), partial(changeReceiverMatch, "class"), partial(changeReciprocityMatch, "class")]

estimateALAAMSA.run_sa(
        G,                                                  # network
        G.binattr["male"],                                  # outcome attr
        param_func_list,                                    # model effects
        [param_func_to_label(f) for f in param_func_list],  # labels for above
        add_gof_param_func_list = gof_funcs                 # effects for GoF
    )
