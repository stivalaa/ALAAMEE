"""
Defines the model in terms of the list of parameters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from functools import partial
from math import log
from changeStatisticsALAAM import *


## Good (but bad gof on TwoStar, ThreeStar)
param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
                   changeContagion,
                   changeTriangleT1, changeTriangleT2, changeTriangleT3,
                   partial(changeoOc, "num_genres"),
                   partial(changeo_Oc, "num_genres")]

