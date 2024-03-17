#!/usr/bin/env python3
#
# File:    run extractModelStats.py
# Author:  Alex Stivala
# Created: April 2023
#
"""Get labels of parameters in the model parameters in model.py
   and write to stdout.

   Usage: extractModelStats.py statfilename

      where statfilename is output of ALAAM simulation e.g.
      extractModelStats.py stats_sim_gof_musae_git.txt

   Note this assumes model.py with param_func_list is present in the cwd
"""
import sys
from changeStatisticsALAAM import *

from modelHR import param_func_list


###
### main
###

if len(sys.argv) != 2:
    sys.stderr.write("USage: " +  sys.argv[0] + " statfilename\n")
    sys.exit(1)

stats_filename = sys.argv[1]

labels =  [param_func_to_label(f) for f in param_func_list]

# always add the t column needed by R scripts
labels += ['t']

# Note in the following,
#  map(list, zip(*[row.split() for row in open(filename).readlines()]))
# reads the data and transposes it so we have a list of columns
# not a list of rows, which then makes it easy to convert to
# the dict where key is column header and value is list of values
# https://stackoverflow.com/questions/6473679/transpose-list-of-lists#

stats  = dict([(col[0], list(col[1:])) for col in map(list, list(zip(*[row.split() for row in open(stats_filename).readlines()])))])

# Select only the columns we want (those in the list of labels from model)
stats = {key: stats[key] for key in labels}

# Probably a neater / trickier way to do this (like above) but this is simple:
sys.stdout.write(" ".join([str(x) for x in labels]) +"\n")
for i in range(len(stats[labels[0]])):
    for j in range(len(labels)):
        statname = labels[j]
        sys.stdout.write(stats[statname][i])
        if j < len(labels)-1:
            sys.stdout.write(" ")
    sys.stdout.write("\n")
