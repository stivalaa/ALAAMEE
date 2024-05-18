"""
Defines the model in terms of the list of parameters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from functools import partial
from math import log
from BipartiteGraph import MODE_A,MODE_B
from changeStatisticsALAAMbipartite import *
from changeStatisticsALAAM import changeoOc,changeo_Oc,changeo_Ob


param_func_list =[partial(changeBipartiteDensity, MODE_A),
                  partial(changeBipartiteGWActivity, MODE_A, log(2)),
                  partial(changeBipartiteAlterTwoStar1,MODE_A),
                  partial(changeBipartiteAlterTwoStar2,MODE_A),
                  partial(changeBipartiteFourCycle1, MODE_A),
                  partial(changeBipartiteFourCycle2, MODE_A),
                  partial(changeoOc, "betweenness.scaled")]

