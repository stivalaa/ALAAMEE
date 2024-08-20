"""
Defines the model in terms of the list of parameters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from functools import partial
from math import log
from changeStatisticsALAAM import *


## [RO] Gof sim bad (no stats in 95% CI):
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
#                   changeContagion,
#                   changeIndirectPartnerAttribute,
#                   changeTriangleT1, changeTriangleT2, changeTriangleT3,
#                   partial(changeoOc, "num_genres"),
#                   partial(changeo_Oc, "num_genres")]

## [RO] Gof sim OK on all but IndirectPartnerAttribute 
## [HU] GoF sim bad (no stats in 95% CI)
param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
                   changeContagion,
                   changeTriangleT1, changeTriangleT2, changeTriangleT3,
                   partial(changeoOc, "num_genres"),
                   partial(changeo_Oc, "num_genres")]

## [RO] gof sim ok (but not great on Density, Activity in particular),
## ok on TwoStar (just), Threestar, PArtnerActivityTwoPath,
## PartnerAttributeActivity, PartnerPartnerAttribute, but 
## bad on IndirectPartnerAttribute:
#param_func_list = [changeDensity, changeActivity,
#                   changeContagion,
#                   changeTriangleT1, changeTriangleT2, changeTriangleT3,
#                   partial(changeoOc, "num_genres"),
#                   partial(changeo_Oc, "num_genres")]

## [RO] Gof sim bad (no stats in 95% CI):
#param_func_list = [changeDensity, changeActivity, changeTwoStar,
#                   changeThreeStar, changeContagion,
#                   changePartnerActivityTwoPath,
#                   changeIndirectPartnerAttribute,
#                   changePartnerAttributeActivity,
#                   changePartnerPartnerAttribute,
#                   partial(changeoOc, "num_genres"),
#                   partial(changeo_Oc, "num_genres")]
#

