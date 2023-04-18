#!/usr/bin/Rscript
#
# File:    convertProject90giantComponentToPajekEdgelist.R
# Author:  Alex Stivala
# Created: April 2023
#
# Based on:
# $Id: convertProject90giantComponentToAdjmatrix.R 538 2016-08-15 04:37:28Z stivalaa $
# from ALAAM snowball sampling project.
#
# Load the Project 90 data and convert the giant component of the 
# network to Pajek format edgelist for ALAAMEE.
#
#
# Usage: RScript convertProject90giantComponentToPajekEdgelist datadir
#
#  datadir is the directory containing the project 90 data
#
#  Output is written to ./project90_giantcomponent.net
#  (WARNING overwritten if it exists)
#

library(igraph)

# read in R source file from directory where this script is located
#http://stackoverflow.com/questions/1815606/rscript-determine-path-of-the-executing-script
source_local <- function(fname){
  argv <- commandArgs(trailingOnly = FALSE)
  base_dir <- dirname(substring(argv[grep("--file=", argv)], 8))
  source(paste(base_dir, fname, sep=.Platform$file.sep))
}

source_local('readProject90Data.R')
source_local('readFiles.R')
source_local('snowballSample.R')

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 1) {
 cat('Usage: Rscript convertProject90giantComponentToAdjmatrix.R datadir\n')
 quit(save="no")
}

datadir <-args[1]

g <- read_project90_data(datadir)
g <- giant.component(g)
print(g)
# See Goel & Salganik 2010 "Assessing respondent-driven sampling"
# PNAS 107(15):6743-6747 [p. 6744 "Data and Methods"]
stopifnot(vcount(g) == 4430) 
stopifnot(ecount(g) == 18407)

write.graph(g, "./project90_giantcomponent.net", format="pajek")

