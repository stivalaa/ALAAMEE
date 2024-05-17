"""
Defines the model in terms of the list of paramters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from functools import partial
from math import log

from BipartiteGraph import MODE_A,MODE_B
from changeStatisticsALAAM import *
from changeStatisticsALAAMbipartite import *

param_func_list = [partial(changeBipartiteDensity, MODE_A),
                   partial(changeoOc, "betweenness.scaled")]
