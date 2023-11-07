
"""
List of change statistics functions for goodness-of-fit,
import from this module so same GoF statistics used for all models.
"""
from functools import partial
from math import log
from changeStatisticsALAAM import *
from changeStatisticsALAAMdirected import *


gof_param_func_list =  [changeDensity,
                        partial(changeGWSender, log(2.0)),
                        partial(changeGWReceiver, log(2.0)),
                        changeLogContagion,
                        changeReciprocity,
                        changeContagionReciprocity,
                        changeMixedTwoStarSource,
                        changeMixedTwoStarSink,
                        partial(changeSenderMatch, "class"),
                        partial(changeReceiverMatch, "class"),
                        partial(changeReciprocityMatch, "class"),
                        changeSender,
                        changeReceiver,
                        changeEgoInTwoStar,
                        changeEgoOutTwoStar,
                        changeMixedTwoStar,
                        changeMixedTwoStarSource,
                        changeMixedTwoStarSink,
                        changeContagion,
                        changeTransitiveTriangleT1,
                        changeTransitiveTriangleT3,
                        changeTransitiveTriangleD1,
                        changeTransitiveTriangleU1,
                        changeCyclicTriangleC1,
                        changeCyclicTriangleC3,
                        changeAlterInTwoStar2,
                        changeAlterOutTwoStar2]

