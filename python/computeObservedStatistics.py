#
# File:    computeObseervedStatistics.py
# Author:  Alex Stivala
# Created: May 2020
#
"""
Compute the observed values of ALAAM statistics by summing the change
statistics for each 1 variable in the outcome variable vector.
"""
import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph,NA_VALUE
from changeStatisticsALAAM import *


def computeObservedStatistics(G, Aobs, changestats_func_list):
    """
    Compute the observed values of ALAAM statistics by summing the change
    statistics for each 1 variable in the outcome variable vector.
    
    Parameters:
       G                   - Graph object for graph to compute stats in
       Aobs                - vector of 0/1 outcome variables for ALAAM
       changestats_func_list-list of change statistics funcions

     Returns:
        numpy vector of observed statistics corresponding to the 
        cangestats_func_list

    """
    # Calculate observed statistics by summing change stats for each 1 variable
    n = len(changestats_func_list)
    Zobs = np.zeros(n)
    Acopy = np.zeros(len(Aobs))
    for i in range(len(Aobs)):
        if Aobs[i] == NA_VALUE:
            Acopy[i] = NA_VALUE
        if Aobs[i] == 1:
            for l in range(n):
                Zobs[l] += changestats_func_list[l](G, Acopy, i)
            Acopy[i] = 1
    assert(np.all(Acopy == Aobs))
    return Zobs
