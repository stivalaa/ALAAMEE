
"""
Defines the model in terms of the list of paramters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from functools import partial
from math import log
from changeStatisticsALAAM import *
from changeStatisticsALAAMdirected import *


## sim gof good on Density, GWSender, GWReceiver, but bad on all others:
param_func_list =  [changeDensity, partial(changeGWSender, log(2.0)), partial(changeGWReceiver, log(2.0)), changeContagion]

## sim gof good on Density, GWSender, GWReceiver, but bad on all others:
#param_func_list =  [changeDensity, partial(changeGWSender, 1.0), partial(changeGWReceiver, 1.0), changeContagion, changeReciprocity, changeContagionReciprocity]

## sim gof good on Density, GWSender, GWReceiover but bad (obs > sim outside 95%) on Contagion
#param_func_list =  [changeDensity, partial(changeGWSender, 0.5), partial(changeGWReceiver, 0.5), changeContagion]

## Does not converge:
#param_func_list =  [changeDensity, partial(changeGWSender, 15.0), partial(changeGWReceiver, 0.1), changeContagion]

## sim gof good on Density, GWSender, GWReceiover but bad (obs > sim outside 95%) on Contagion
#param_func_list =  [changeDensity, partial(changeGWSender, 5.0), partial(changeGWReceiver, 1.0), changeContagion]

## not good convergence on GWContagion (never is it seems)
## Bad gof sim on GWContagion (negative values - should not even be possible)
#param_func_list =  [changeDensity, partial(changeGWSender, 1.0), partial(changeGWReceiver, 1.0),  partial(changeGWContagion, 1.0)]

## sim gof good on Density, GWSender, GWReceiover but bad (obs > sim outside 95%) on Contagion
#param_func_list =  [changeDensity, partial(changeGWSender, 1.0), partial(changeGWReceiver, 5.0),  changeContagion]

###(back to learningRate = 0.001) above here)
## Bad sim gof on all (learningRate = 0.01):
#param_func_list =  [changeDensity, partial(changeGWSender, 1.0), partial(changeGWReceiver, 5.0),  changeContagion]

### learningRate = 0.001 below here:
## still sim gof OK on density, GWSender (very small values for this stat now), GWReceiver, bad on Contagion:
#param_func_list =  [changeDensity, partial(changeGWSender, 5.0), partial(changeGWReceiver, 5.0),  changeContagion]
## sim gof OK on density, GWSender, GWReceiver, bad on Contagion:
#param_func_list =  [changeDensity, partial(changeGWSender, 0.2), partial(changeGWReceiver, 0.2),  changeContagion]
## sim gof OK on density, GWSender, GWReceiver, bad on Contagion:
#param_func_list =  [changeDensity, partial(changeGWSender, 2.0), partial(changeGWReceiver, 2.0),  changeContagion]


## sim gof OK on Desnity, GWSEnder, GWReceiver, but bad on Contagion:
#[changeDensity, changeContagion, changeGWSender, changeGWReceiver],
#["Density",      "Contagion",    "GWSender",     "GWReceiver"],
## Bad sim gof on all:
#[changeDensity, changeContagion, changeSender, changeReceiver],
#["Density",      "Contagion",    "Sender",     "Receiver"],
## Bad sim gof on Contagion (But OK on Density and Sender); for not in params, good on REciprocity, EgoInTwoStar, OK on Contagion reciprocity (but bad on EgouOutTwoStar)
#[changeDensity, changeContagion, changeSender],
#["Density",      "Contagion",    "Sender"],
# bad sim gof on all:
#[changeDensity, changeContagion, changeEgoInTwoStar, changeEgoOutTwoStar, changeReciprocity, changeContagionReciprocity],
#["Density",      "Contagion",    "EgoInTwoStar",     "EgoOutTwoStar",     "Reciprocity",     "ContagionReciprocity"],
# sim Gof good on Density, borderline (bad) on contagion (for not in params; goo don Recevier but bad on Sender):
#[changeDensity, changeContagion],
#["Density",      "Contagion"],
## Bad gof sim:
#[changeDensity, changeContagion, changeSender, changeReceiver],
# ["Density",      "Contagion",    "Sender",     "Receiver"],
