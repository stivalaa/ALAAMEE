#!/usr/bin/Rscript
#
# File:    snowballSampleFromExampleData.R
# Author:  Alex Stivala
# Created: September 2015
#
# Read network and attributes and set of outcome files (ALAAM simulation model) 
# and take snowball sample, writing out the new newtork
# and attributes and outcomes files.
#
# Usage: Rscript snowballSampleFromExampleData.R num_waves num_seeds networkFilename binAttrFileName contAttrFileName outcomeFile
#
#    num_waves              - number of snowball waves            
#    num_seeds             - number of snowball seeds
#    networkFileName       - network file name  (Pajek edgelist)
#    binAttrFileName       - binary attribute file name
#    contAttrFileName      - continuous attribute file name
#    outcomeFile           - filename outcome binary attribute 
#
# Output files are in cwd, basename of input files with _wavesX_seedsY
# appended before suffix,  where X is number of waves,
# and Y is number of seeds e.g. waves2_seeds3
# Also  snowball_zonefile with suffixies above
# snowball_zonefile shows the snowball sample zone of each node from
# snowball_sample() procedure
#
#  E.g.: Rscript ../../R/snowballSampleFromExampleData.R 2 3 ../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt ../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt ../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt  ../data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt
#
# 

library(igraph)

# read in R source file from directory where this script is located
#http://stackoverflow.com/questions/1815606/rscript-determine-path-of-the-executing-script
source_local <- function(fname){
  argv <- commandArgs(trailingOnly = FALSE)
  base_dir <- dirname(substring(argv[grep("--file=", argv)], 8))
  source(paste(base_dir, fname, sep=.Platform$file.sep))
}

source_local('readFiles.R')
source_local('snowballSample.R')

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 6) {
 cat('Usage: Rscript snowballSampleFromExampleData.R num_waves num_seeds networkFilename binAttrFileName contAttrFileName outcomeFilePattern\n')
 quit(save="no")
}
num_waves <- as.integer(args[1])
num_seeds <- as.integer(args[2])
networkFilename <-args[3]
binAttrFilename <- args[4]
contAttrFilename <- args[5]
outcomeFilename <- args[6]

cat("number of seeds: ", num_seeds, "\n")
cat("number of waves: ", num_waves,"\n")



suffix <- paste('_waves', num_waves, '_seeds', num_seeds, sep='')
networkBasename <- sub("(.+)[.].+", "\\1", basename(networkFilename))
binAttrBasename <- sub("(.+)[.].+", "\\1", basename(binAttrFilename))
contAttrBasename <- sub("(.+)[.].+", "\\1", basename(contAttrFilename))

g <- read_graph_file(networkFilename, directed=FALSE)
V(g)$binAttr <- read_attr_file(binAttrFilename)
V(g)$contAttr <- read_attr_file(contAttrFilename)

V(g)$outcome <- read_outcome_file(outcomeFilename)
seed_nodes <- sample.int(vcount(g), num_seeds, replace=FALSE)
g <- snowball_sample(g, num_waves, seed_nodes)
outcomeBasename <- sub("(.+)[.].+", "\\1", basename(outcomeFilename))
samplenum <- sub(".+[a-z]([0-9]+)[.].+", "\\1", basename(outcomeFilename))
samplesuffix <- paste('_num', samplenum, sep='')
outcomeOutputFilename <- paste(outcomeBasename, suffix, '.txt', sep='')
networkOutputFilename <- paste(networkBasename, suffix, samplesuffix, '.txt', sep='')
binAttrOutputFilename <- paste(binAttrBasename, suffix, samplesuffix, '.txt', sep='')
contAttrOutputFilename <- paste(contAttrBasename, suffix, samplesuffix, '.txt', sep='')
fakezoneOutputFilename <- paste('zonefile', suffix, samplesuffix, '.txt', sep='')
zoneOutputFilename <- paste('snowball_zonefile', suffix, samplesuffix, '.txt', sep='')

cat("writing sampled network edgelist to", networkOutputFilename, "\n")
write_graph(g, networkOutputFilename, format="pajek")
cat("writing sampled network binary node attributes to", binAttrOutputFilename, "\n")
write_attr_file(binAttrOutputFilename, V(g)$binAttr, "binaryAttribute")
cat("writing sampled network continuous node attributes to", contAttrOutputFilename, "\n")
write_attr_file(contAttrOutputFilename, V(g)$contAttr, "continuousAttribute")
cat("writing sample network binary outcome node attributes to", outcomeOutputFilename, "\n")
write_outcome_file(outcomeOutputFilename, V(g)$outcome)

                                        # snowball sample node zones
cat("writing sample network node zones to", zoneOutputFilename, "\n")
write_zone_file(zoneOutputFilename, V(g)$zone)

