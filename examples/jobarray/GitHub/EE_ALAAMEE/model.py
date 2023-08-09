"""
Defines the model in terms of the list of paramters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from functools import partial
from math import log
from changeStatisticsALAAM import *


## does not converge with GWContagin (as always it seems) [bad trace plot, gof sim shows GWContagion not converging)
param_func_list = [changeDensity, partial(changeGWActivity, 2.0), partial(changeGWContagion, 2.0)]
## good gof sim on Density, only OK on Contagion, but bad on GWActivity:
#param_func_list = [changeDensity, partial(changeGWActivity, 0.1), changeContagion]
## very good gof sim on Density,Contagion, but bad on GWActivity:
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0), changeContagion]
## good gof sim on Density,Contagion, but bad on GWActivity:
#param_func_list = [changeDensity, partial(changeGWActivity, log(2.0)), changeContagion]


### with learningRate = 0.001:
#[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion],
#["Density",     "Activity",     "Two-Star",    "Three-Star",   "Contagion"],
## Does not converge:
#[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion],
#["Density",     "Activity",     "Two-Star",    "Three-Star",   "Contagion"],
## Extremely slow (very low acceptance rate), did not finish:
#[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeContagion, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute],
#["Density", "Activity", "Two-Star", "Three-Star", "Alter-2Star1", "Contagion", "Alter-2Star2", "Partner-Activity", "Partner-Resource"],
## Bad GoF sim:
#[changeDensity, changeActivity,   changeContagion],
#["Density",     "Activity",       "Contagion"],
## Does not converge:
#[changeDensity, changeActivity, changeTwoStar,  changeContagion],
#["Density",     "Activity",     "Two-Star",    "Contagion"],
### with default learningRate = 0.01:
## Bad GoF sim:
#[changeDensity, changeActivity,   changeContagion],
#["Density",     "Activity",       "Contagion"],
## Does not converge:
#[changeDensity, changeActivity, changeTwoStar,  changeContagion],
#["Density",     "Activity",     "Two-Star",    "Contagion"],
## Does not converge:
#[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion],
#["Density",     "Activity",     "Two-Star",    "Three-Star",   "Contagion"],
#[changeDensity, changeActivity, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeContagion, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute],
#["Density", "Activity", "Two-Star", "Three-Star", "Alter-2Star1", "Contagion", "Alter-2Star2", "Partner-Activity", "Partner-Resource"],
