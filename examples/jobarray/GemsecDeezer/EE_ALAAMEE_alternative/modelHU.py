"""
Defines the model in terms of the list of parameters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from functools import partial
from math import log
from changeStatisticsALAAM import *

## [HU] GoF sim bad (well outside 95% CI) on all but GWActivity(2)
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
#                   partial(changePowerContagion, 2),
#                   changeTriangleT1, changeTriangleT2, changeTriangleT3,
#                   partial(changeoOc, "num_genres"),
#                   partial(changeo_Oc, "num_genres")]

## [HU] GoF sim OK on model parameters and also others
## (particularly Activity) except Contagion, IndirectPartnerAttribute,
## PartnerAttributeActivity, ParterPartnerAttribute, T3 (But T1, T2 OK)
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
#                   partial(changePowerContagion, 2),
#                   partial(changeoOc, "num_genres"),
#                   partial(changeo_Oc, "num_genres")]

## [HU] GoF sim good in model parameters, bad on all others
## (except IndirectPartnerAttribute and PartnerAttributeActivity, T2; OK)
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
#                   partial(changePowerContagion, 2),
#                   partial(changeoOc, "num_genres")]

## [HU] GoF sim OK in model parameters, bad on all others
param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
                   changeContagion,
                   partial(changeoOc, "num_genres")]

## [HU] GoF sim OK in model parameters, bad on all others
## (except PartnerPArtnerAttribute, T2, T3, but not T1, OK)
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
#                   changeContagion]


## [HU] GoF sim bad (no stats in 95% CI)
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
#                   changeContagion,
#                   partial(changeoOc, "num_genres"),
#                   partial(changeo_Oc, "num_genres")]

## [RO] gof sim ok (but not great on Density, Activity in particular),
## ok on TwoStar (just), Threestar, PArtnerActivityTwoPath,
## PartnerAttributeActivity, PartnerPartnerAttribute, but 
## bad on IndirectPartnerAttribute:
## [HU] GoF sim bad (no stats in 95% CI)
#param_func_list = [changeDensity, changeActivity,
#                   changeContagion,
#                   changeTriangleT1, changeTriangleT2, changeTriangleT3,
#                   partial(changeoOc, "num_genres"),
#                   partial(changeo_Oc, "num_genres")]


## [RO] Gof sim OK on all but IndirectPartnerAttribute 
## [HU] GoF sim bad (no stats in 95% CI)
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
#                   changeContagion,
#                   changeTriangleT1, changeTriangleT2, changeTriangleT3,
#                   partial(changeoOc, "num_genres"),
#                   partial(changeo_Oc, "num_genres")]


