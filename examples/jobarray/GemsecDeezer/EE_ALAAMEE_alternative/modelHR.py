"""
Defines the model in terms of the list of parameters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from functools import partial
from math import log
from changeStatisticsALAAM import *


## [HR] sim gof ok (in 95% CI) on all (density abs t-ratio > 1.5 though)
param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
                   changeContagion,
                   partial(changeoOc, "num_genres"),
                   partial(changeo_Oc, "num_genres")]


## [RO] Gof sim OK on all but IndirectPartnerAttribute 
## [HR] GoF sim bad (well oustide 95% CI) on all but GWActivity(2) which is good
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
#                   changeContagion,
#                   changeTriangleT1, changeTriangleT2, changeTriangleT3,
#                   partial(changeoOc, "num_genres"),
#                   partial(changeo_Oc, "num_genres")]

