#!/usr/bin/env python3
#
# File:    run ALAAMEEpokecParallel.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. This version takes run number parameter so that
 parallel runs can be run with GNU parallel. 
 Usage:
     runALAAMEEpokecParallel.py runNumber
"""
import getopt
import sys
from functools import partial

import  estimateALAAMEE
from changeStatisticsALAAM import *
from changeStatisticsALAAMdirected import *

from model import param_func_list

def usage(progname):
    """
    print usage msg and exit
    """
    sys.stderr.write("usage: " + progname + " runNumber\n")
    sys.exit(1)


def main():
    """
    See usage message in module header block
    """
    try:
        opts,args = getopt.getopt(sys.argv[1:], "")
    except:
        usage(sys.argv[0])
    for opt,arg in opts:
        usage(sys.argv[0])

    if len(args) != 1:
        usage(sys.argv[0])

    runNumber = int(args[0])

    estimateALAAMEE.run_on_network_attr(
        '../data/soc-pokec-relationships-directed.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        ### With learningRate = 0.001:
        # bad sim gof on Contagion, but good on others in model:
        #[changeDensity, changeContagion, partial(changeoOc, "age"), changeSender, changeReceiver],
        #["Density",      "Contagion",     "age_oOc",                 "Sender",     "Receiver"],
        ## Bad sim gof on Receiver and Contagion (OK but not great on Density, Reciprocity, age; OK on Sender); also OK on MixedTwoStar although not in model:
        #[changeDensity, changeContagion, partial(changeoOc, "age"), changeSender, changeReceiver,  changeReciprocity],
        #["Density",      "Contagion",     "age_oOc",                 "Sender",     "Receiver",     "Reciprocity"],
        ## Bad sim gof on all parameters (but good on MixTwoStar):
        #[changeDensity, changeContagion, partial(changeoOc, "age"), changeSender, changeReceiver, changeEgoInTwoStar, changeEgoOutTwoStar, changeContagionReciprocity],
        #["Density",      "Contagion",     "age_oOc",                 "Sender",     "Receiver",     "EgoInTwoStar",     "EgoOutTwoStar",     "ContagionReciprocity"],
        ## Good sim gof on parameters (also Receiver):
        #[changeDensity, changeContagion, partial(changeoOc, "age")],
        #"Density", "Contagion", "age_oOc"],

        ### Old (default learningRate = 0.01)
        #[changeDensity, changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar,  partial(changeoOc, "age"), changeContagionReciprocity, partial(changeSenderMatch, "region"), partial(changeReceiverMatch, "region"), partial(changeReciprocityMatch, "region")],
        #["Density",     "Sender",     "Receiver",     "Reciprocity",     "EgoInTwoStar",     "EgoOutTwoStar",     "MixedTwoStar",      "age_oOc",                 "ContagionReciprocity",     "region_SenderMatch",                 "region_ReceiverMatch",                 "region_ReciprocityMatch"],
        ## Converges OK:
        #[changeDensity, changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar,  partial(changeoOc, "age"), changeContagionReciprocity, partial(changeSenderMatch, "region"), partial(changeReceiverMatch, "region"), partial(changeReciprocityMatch, "region")],
        #["Density",     "Sender",     "Receiver",     "Reciprocity",     "EgoInTwoStar",     "EgoOutTwoStar",     "MixedTwoStar",      "age_oOc",                 "ContagionReciprocity",     "region_SenderMatch",                 "region_ReceiverMatch",                 "region_ReciprocityMatch"],
        #[changeDensity, changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar,  partial(changeoOc, "age"), changeContagionReciprocity],
        #["Density",     "Sender",     "Receiver",     "Reciprocity",     "EgoInTwoStar",     "EgoOutTwoStar",     "MixedTwoStar",      "age_oOc",                 "ContagionReciprocity"],
        #[changeDensity, changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar,  partial(changeoOc, "age")],
       # ["Density",     "Sender",     "Receiver",     "Reciprocity",     "EgoInTwoStar",     "EgoOutTwoStar",     "MixedTwoStar",      "age_oOc"],
        ## Does not converge:
        #[changeDensity, changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar,  partial(changeoOc, "age"), changeContagionReciprocity, partial(changeSenderMatch, "region"), partial(changeReceiverMatch, "region"), partial(changeReciprocityMatch, "region"), changeTransitiveTriangleT3],
        #["Density",     "Sender",     "Receiver",     "Reciprocity",     "EgoInTwoStar",     "EgoOutTwoStar",     "MixedTwoStar",      "age_oOc",                 "ContagionReciprocity",     "region_SenderMatch",                 "region_ReceiverMatch",                 "region_ReciprocityMatch",                 "TransitiveTriangleT3"],
        ##[changeDensity, changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar, changeContagion,  partial(changeoOc, "age")],
        ##["Density",     "Sender",     "Receiver",     "Reciprocity",     "EgoInTwoStar",     "EgoOutTwoStar",     "MixedTwoStar",     "Contagion",      "age_oOc"],
        ##[changeDensity, changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar, changeContagion, changeContagionReciprocity,  partial(changeoOc, "age")],
        ##["Density",     "Sender",     "Receiver",     "Reciprocity",     "EgoInTwoStar",     "EgoOutTwoStar",     "MixedTwoStar",     "Contagion",     "ContagionReciprocity",      "age_oOc"],
        ##[changeDensity, changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar, changeContagion, changeContagionReciprocity,  changeAlterOutTwoStar2, partial(changeoOc, "age")],
        ##["Density",     "Sender",     "Receiver",     "Reciprocity",     "EgoInTwoStar",     "EgoOutTwoStar",     "MixedTwoStar",     "Contagion",     "ContagionReciprocity",     "AlterOutTwoStar2",      "age_oOc"],
        ##[changeDensity, changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar, changeContagion, changeContagionReciprocity, changeTransitiveTriangleT3, changeCyclicTriangleC3, changeAlterOutTwoStar2, partial(changeoOc, "age")], # partial(changeoO_Osame, "region")],
        ##["Density",     "Sender",     "Receiver",     "Reciprocity",     "EgoInTwoStar",     "EgoOutTwoStar",     "MixedTwoStar",     "Contagion",     "ContagionReciprocity",     "TransitiveTriangleT3",     "CyclicTriangleC3",     "AlterOutTwoStar2",     "age_oOc"], #,                 "region_oO_Osame"],

        '../data/soc-pokec-binattr.txt',  # use male as outcome variable
        None, #'../data/soc-pokec-binattr.txt',
        '../data/soc-pokec-contattr.txt',
        '../data/soc-pokec-catattr.txt',
        run = runNumber,
        learningRate = 0.001,
        directed = True
        )


if __name__ == "__main__":
    main()


