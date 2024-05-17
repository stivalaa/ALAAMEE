
"""
List of change statistics functions for goodness-of-fit,
import from this module so same GoF statistics used for all models.
"""
from functools import partial
from math import log

from BipartiteGraph import MODE_A,MODE_B
from changeStatisticsALAAM import *
from changeStatisticsALAAMbipartite import *

gof_funcs = [partial(changeBipartiteDensity, MODE_A),
         partial(changeBipartiteActivity, MODE_A),
         partial(changeBipartiteEgoTwoStar, MODE_A),
         partial(changeBipartiteEgoThreeStar, MODE_A),
         partial(changeBipartiteAlterTwoStar1,MODE_A),
         partial(changeBipartiteAlterTwoStar2,MODE_A),
         partial(changeBipartiteFourCycle1, MODE_A),
         partial(changeBipartiteFourCycle2, MODE_A),
         partial(changeoOc, "betweenness.scaled"),
         partial(changeoOc, "harmonic.cent.scaled"),
         partial(changeoOc, "birank.scaled")]
