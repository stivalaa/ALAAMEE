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
         partial(changeBipartiteActivity, MODE_A),
         partial(changeBipartiteEgoTwoStar, MODE_A),
         partial(changeBipartiteEgoThreeStar, MODE_A),
         partial(changeBipartiteAlterTwoStar1,MODE_A),
         partial(changeBipartiteAlterTwoStar2,MODE_A),
         partial(changeBipartiteFourCycle1, MODE_A),
         partial(changeBipartiteFourCycle2, MODE_A),
         partial(changeoOc, "birank.scaled")]
