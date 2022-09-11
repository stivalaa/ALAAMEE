#!/usr/bin/env python3
#
# File:    runALAAMSAkarateClub.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the Zachary Karate Club example.
"""

from functools import partial
import  estimateALAAMSA
from changeStatisticsALAAM import *

estimateALAAMSA.run_on_network_attr(
    '../data/karate_club/karate.net',
    [changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion, changeTriangleT1, changeTriangleT2, changeTriangleT3, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute, partial(changeoOb, "senior"), partial(changeo_Ob, "senior"), partial(changeoOc, "age"), partial(changeo_Oc, "age"), partial(changeoO_Osame, "gender")],
    ["Density", "Activity", "Star2", "Star3", "Contagion", "T1", "T2", "T3", "2-Path-Equivalence", "Partner-Attribute-Activity", "Partner-Resource", "senior_oOb", "senior_o_Ob", "age_oOc", "age_o_Oc", "gender_match"],
    '../data/karate_club/karate_outcome.txt',
    '../data/karate_club/karate_binattr.txt',
    '../data/karate_club/karate_contattr.txt',
    '../data/karate_club/karate_catattr.txt'
    )



