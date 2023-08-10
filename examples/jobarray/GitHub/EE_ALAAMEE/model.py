"""
Defines the model in terms of the list of paramters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from functools import partial
from math import log
from changeStatisticsALAAM import *



#slow (did not finish): param_func_list = [changeDensity, partial(changeGWActivity, log(2.0)), changeContagion, changePartnerActivityTwoPath, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute]

## bad sim gof on all parameters:
#param_func_list = [changeDensity, partial(changeGWActivity, log(2.0)), changeContagion, changePartnerActivityTwoPath]

## (very) bad gof sim on all parameters (learningRate = 0.01)
## [same if learningRate = 0.001]:
#param_func_list = [changeDensity, changeActivity, changeContagion]

## good convergence and sim gof on parameters in model (learningRate = 0.01):
param_func_list = [changeDensity, partial(changeGWActivity, log(2.0)), changeContagion]

### Below with learningRate = 0.001 (did not converge properly in default iterations)
## not good convergence, bad sim gof on GWActivity:
#param_func_list = [changeDensity, partial(changeGWActivity, 5.0), changeContagion]
## does not converge with GWContagin (as always it seems) [bad trace plot, gof sim shows GWContagion not converging)
#param_func_list = [changeDensity, partial(changeGWActivity, 2.0), partial(changeGWContagion, 2.0)]
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
