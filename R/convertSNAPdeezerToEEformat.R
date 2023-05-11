##!/usr/bin/Rscript
##
## File:    convertSNAPdeezerToALAAMEEFormat.R
## Author:  Alex Stivala
## Created: May 2023
##
## Read the network and attributes data for the Deezer Europe social
## network from SNAP http://snap.stanford.edu/data/deezer_europe.zip
## and convert to Pajek format for ALAAMEE or EstimNetDirected.  See
## documentation in
## http://snap.stanford.edu/data/feather-deezer-social.html and source
## citation:
##
## Rozemberczki, B., & Sarkar, R. (2020, October). Characteristic
## functions on graphs: Birds of a feather, from statistical
## descriptors to parametric models. In Proceedings of the 29th ACM
## international conference on information & knowledge management
## (pp. 1325-1334).
#
## Reference for SNAP collection of data sets:
## 
##@misc{snapnets,
##  author       = {Jure Leskovec and Andrej Krevl},
##  title        = {{SNAP Datasets}: {Stanford} Large Network Dataset Collection},
##  howpublished = {\url{http://snap.stanford.edu/data}},
##  month        = jun,
##  year         = 2014
##}
##
##
## Usage:
## 
## Rscript convertSNAPdeezerToALAAMEEFormat.R deezer_europe.zip
##
## deezer_europe.zip is the zip file downloaded from
## http://snap.stanford.edu/data/deezer_europe.zip
##
## Output files in cwd (WARNING overwritten):
##   deezer_europe.net
##   deezer_europe_target.net
##

library(igraph)

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 1) {
  cat("Usage: convertSNAPdeezerToALAAMEEFormat.R deezer_europe.zip\n")
  quit(save="no")
}
zipfile <- args[1]

## zipfile contents:
## unzip -t ~/SwitchDrive/Institution/USI/datasets/SNAP_Datasets/feather-deezer-social/deezer_europe.zip 
## Archive:  /home/alex/SwitchDrive/Institution/USI/datasets/SNAP_Datasets/feather-deezer-social/deezer_europe.zip
##     testing: deezer_europe/           OK
##     testing: deezer_europe/README.txt   OK
##     testing: deezer_europe/deezer_europe_edges.csv   OK
##     testing: deezer_europe/deezer_europe_features.json   OK
##     testing: deezer_europe/deezer_europe_target.csv   OK
## No errors detected in compressed data of /home/alex/SwitchDrive/Institution/USI/datasets/SNAP_Datasets/feather-deezer-social/deezer_europe.zip.

## From the README.txt in zip file:
##
##  A social network of Deezer users which was collected from the
##  public API in March 2020. Nodes are Deezer users from European
##  countries and edges are mutual follower relationships between
##  them. The vertex features are extracted based on the artists liked
##  by the users. The task related to the graph is binary node
##  classification - one has to predict the gender of users. This
##  target feature was derived from the name field for each user.
##
##  Statistics:
##
##  Nodes 28,281
##  Edges 92,752
##  Density 0.0001
##  Transitivity 0.0959

## From http://snap.stanford.edu/data/feather-deezer-social.html
##
##  Dataset statistics
##  Directed	No.
##  Node features	Yes.
##  Edge features	No.
##  Node labels	Yes. Binary class.
##  Temporal	No.
##  Nodes	28,281
##  Edges	92,752
##  Density	0.0002
##  Transitvity	0.0959
##

## See also https://github.com/benedekrozemberczki/FEATHER
## for original copy of data and more documentation


outfilename_undirected <- "deezer_europe.net"
targetfilename <- "deezer_europe_target.txt"

##
## network
##
edgelist <- read.table(unz(zipfile,
                           'deezer_europe/deezer_europe_edges.csv'),
                       header = TRUE,  stringsAsFactors = FALSE, sep = ',')

uniqueIds <- unique(c(edgelist$node_1, edgelist$node_2))
numIds <- length(uniqueIds)
cat('number of unique ids is ', numIds, '\n')
cat('min is ', min(uniqueIds), ' max is ', max(uniqueIds), '\n')


## The Deezer data has nodes numbered 0..N-1 (N = 28281)
stopifnot(min(uniqueIds) == 0)
stopifnot(max(uniqueIds) == numIds - 1)
stopifnot(numIds == 28281)

## have to add 1 as igraph cannot handle 0 as vertex id apparently
g <- graph.edgelist(as.matrix(edgelist)+1, directed=FALSE)


summary(g)
## remove multiple and self edges
g <- simplify(g , remove.multiple = TRUE, remove.loops = TRUE)
summary(g)


##  Nodes 28,281
##  Edges 92,752
stopifnot(vcount(g) == 28281)
stopifnot(ecount(g) == 92752)


##
## read binary target attribute This target feature, gender, was
## derived from the name field.
##

target <- read.table(unz(zipfile,
                         'deezer_europe/deezer_europe_target.csv'),
                     header = TRUE, stringsAsFactors = FALSE, sep = ',')
## Make sure it really does line up with the node ids 0..N-1
stopifnot(nrow(target) == numIds)
stopifnot(min(target$id) == 0)
stopifnot(max(target$id) == numIds - 1)

##
## get binary attributes
##

## TODO there seems to be no documentation of how this is coded,
## neither in the README or in the paper: is 1 for male or female?

outcomebinattr <- data.frame(gender = target[, "target"]) 
summary(outcomebinattr)


## TODO read and process deezer_europe_features.json This JSON format
## file gives a list of features (integers) based on artist liked by
## users. So this could then be used as attribute for categorical set
## similarity (Jaccard) in EstimNetDirected.


##
## Write network
##
write.graph(g, outfilename_undirected, format="pajek")


##
## write outcome binary attribute
##

write.table(outcomebinattr, file = targetfilename, row.names = FALSE,
            col.names = TRUE, quote = FALSE)
