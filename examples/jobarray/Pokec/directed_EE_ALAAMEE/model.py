"""
Defines the model in terms of the list of paramters to estimate
(also used for computing observed statistics and simulation for GoF)
"""
from math import log
from functools import partial
from changeStatisticsALAAM import *
from changeStatisticsALAAMdirected import *

## Good sim gof on all in model, not good on other stats not in model (SEnder, REciver, EgoInTwoStar, EgoOutTwoSTar, MixedTwoStar):
param_func_list =  [changeDensity, changeContagion, partial(changeoOc, "age"), partial(changeGWSender, log(2.0)), partial(changeGWReceiver, log(2.0)), changeReciprocity, changeContagionReciprocity]

## Good sim gof on Density, Contagion, GWSender, but not as good as log(2) on GWReceiver [still in 95% though]; bad on all other stats not in model including Sender,Receiver,REciprocity,ContationReciprocity
#param_func_list =  [changeDensity, changeContagion, partial(changeoOc, "age"), partial(changeGWSender, 0.2), partial(changeGWReceiver, 0.2)]

## Good sim gof on Density, Contagion, GWSender, GWReceiver (first try!); bad on all other stats not in model including Sender,Receiver,REciprocity,ContationReciprocity
#param_func_list =  [changeDensity, changeContagion, partial(changeoOc, "age"), partial(changeGWSender, log(2.0)), partial(changeGWReceiver, log(2.0))]
