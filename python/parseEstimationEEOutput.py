#
# File:    parseEstimationEEOutput.py
# Author:  Alex Stivala
# Created: August 2023
#
"""Parse the output of the computeALAMEEcovariance.R R script
"""

from itertools import islice,dropwhile

def parseEstimationEEOutput(filename):
    """Parse output of the computeALAAMEEcovariance.R R script.

    Parameters:
        filename - filename of the output of computeALAAMEEcovariance.R to read

    Return value:
        tuple (paramname_list, estimate_list)
        where paramname_list is list of parameter names, and
        estimate_list is list of point estimates corresponding to them, e.g:
        (['Density', 'GWSender.0.6931471805599453', 'GWReceiver.0.6931471805599453', 'Contagion'], ['0.01212774', '-0.06600637', '-0.01503764', '-6.485873e-05'])
    """
    # The output looks like this, written from R with
    #   cat(paramname, pooled_est$estimate, sd(theta[,paramname]), 
    #   pooled_est$se, est_t_ratio, signif, '\n'):
    #
    # Run  0
    # Density 0.01206792 0.002983711 0.05822977 0.0165434
    # GWSender.0.6931471805599453 -0.06553917 0.01575737 0.578148 -0.004427593
    #...
    # Pooled
    # Density 0.01212774 0.002957743 0.04333061 -0.006650219
    # GWSender.0.6931471805599453 -0.06600637 0.01634581 0.3849595 -0.02848913
    # GWReceiver.0.6931471805599453 -0.01503764 0.004703949 0.08361433 -0.001180339
    # Contagion -6.485873e-05 0.0002813753 0.0007355613 0.008571341
    # TotalRuns 2
    # ConvergedRuns 2
    #

    retlist = []
    with open(filename, 'r') as f:
        while not next(f).startswith('Pooled'):
            pass
        for line in f:
            if line.startswith("TotalRuns"):
                break
            s = line.split(" ")
            paramname   = s[0]
            estimate    = float(s[1])
            sd_estimate = float(s[2])
            std_error   = float(s[3])
            est_t_ratio = float(s[4])
            retlist.append((paramname, estimate))

    # Convert list of tuples to tuple of lists
    #https://stackoverflow.com/questions/8081545/how-to-convert-list-of-tuples-to-multiple-lists
    return tuple(map(list, zip(*retlist)))
