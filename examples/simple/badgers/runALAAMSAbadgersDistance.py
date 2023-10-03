#!/usr/bin/env python3
#
# File:    runALAAMSAbadgersDistance.py
# Author:  Alex Stivala
# Created: May 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the undirected network

 See README file and convertBadgerDataToALAAMEEFormat.R in ./data/
 directory for more details, as well as:

     Silk, M. J., Croft, D. P., Delahay, R. J., Hodgson, D. J.,
     Weber, N., Boots, M., & McDonald, R. A. (2017). 
     The application of statistical network models in disease research. 
     Methods in Ecology and Evolution, 8(9), 1026-1041.
 

This model is similar to the network autocorrelation model in the S.I.
of the above paper (included in zip file in data directory).

"""
import io,csv
from zipfile import ZipFile
import numpy as np
from functools import partial
import  estimateALAAMSA
from changeStatisticsALAAM import *
from utils import int_or_na,float_or_na,NA_VALUE


def changeContagionDist(distmatrix, G, A, i):
    """Change statistic for ContagionDist, outcome attribute on two actors
    related to the distance betwen them
    
    *...*
    
    (where '...' denotes the distance as specified in distmatrix).
    The distance matrix distmatrix is an NxN numpy matrix (where N is
    the number of nodes in G) where distmatrix[i,j] is the distance
    beetween nodes i and j.

    """
    delta = 0
    for u in G.neighbourIterator(i):
        if A[u] == 1:
            delta += distmatrix[i, u]
    return delta


##############################################################################
##
## Main
##
##############################################################################


# read group (sett) locations from CSV file in Silk et al. (2018) S.I. zipfile
# (all the other data has already been read and converted to correct format
# for estimateALAAMSA.run_on_network_attr() by
# running data/convertBadgerDataToALAAMEEFormat.R)
with ZipFile("data/mee312770-sup-0001-supinfo.zip", "r") as zf:
    with zf.open("grouplocsSAOM.csv", "r") as infile:
        csviter = csv.reader(io.TextIOWrapper(infile, "utf-8"))
        # Sett,Group,X,Y
        # Sett is name, Group is 1..6 as used in categorical attribute
        colnames = next(csviter)
        # Convert to dict mapping Group to (X, Y)
        grouploc_dict = dict([(int(row[1]), tuple([float(x) for x in row[2:]])) for row in csviter])

print("grouploc_dict =", grouploc_dict)#XXX

catattr_filename = 'data/badgers_catattr.txt'

# Read categorical attributes
# This is a copy of line from Graph.py and read from filename in call
# to run_on_network_attr() below, but we also need it here.
catattr = dict([(col[0], list(map(int_or_na, col[1:]))) for col in map(list, list(zip(*[row.split() for row in open(catattr_filename).readlines()])))])
groups = catattr["group"]

print("groups = ", groups)#XXX

# Now use groups and group locations to give (X,Y) location for
# each individual, which is just that of the group they are in
locations = [grouploc_dict[group] for group in groups]

print("locations = ", locations)#XXX


# and build a distance matrix, using this trick of using the complex
# type (since Python/numpy has nothing liek the R dist() function, and
# I am not going to the hassle of trying to install scipy again):
# https://stackoverflow.com/questions/22720864/efficiently-calculating-a-euclidean-distance-matrix-using-numpy
z = np.array([complex(loc[0], loc[1]) for loc in locations])
m, n = np.meshgrid(z, z)
distmatrix = abs(m - n)
print("dim distmatrix = ", np.shape(distmatrix))#XXX
print("distmatrix = ", distmatrix)#XXX



param_func_list =  [changeDensity, changeActivity, changeContagion, 
                    partial(changeoOb, "male"),
                    partial(changeoOb, "yearling"),
                    partial(changeoO_Osame, "group"),
                    partial(changeoO_OsameContagion, "group"),
                    partial(changeContagionDist, distmatrix)]

print("parameters: ",[param_func_to_label(f) for f in param_func_list])#XXX

estimateALAAMSA.run_on_network_attr(
        'data/badgers_overallnetwork.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        outcome_bin_filename = 'data/badgers_TBpos.txt',
        binattr_filename = 'data/badgers_binattr.txt',
        contattr_filename = 'data/badgers_contattr.txt',
        catattr_filename = catattr_filename,
        directed = False
    )
