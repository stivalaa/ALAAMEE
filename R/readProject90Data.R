# 
# File:    readProject90Data.R
# Author:  Alex Stivala
# Created: Augstu 2016
#
# $Id: readProject90Data.R 537 2016-08-15 04:23:42Z stivalaa $
# 
# Function to load the Projectc 90 (Colorado Spring) node and edge
# TSV files and convert to igraph format
# for use in R with statnet and to save externally for Snowball PNet etc.
#
# Data downloaded from Princeton Office of Population Research.
# http://opr.princeton.edu/archive/restricted
#

library(igraph)

# node attribute names in the Project 90 data (not including id)
project90_attr_names <-  c('race','gender','sex.worker','pimp','sex.work.client','drug.dealer','drug.cook','thief','retired','housewife','disabled','unemployed','homeless')

# categorical attribute names (all the rest are binary)
project90_categorical_attr_names <- c('race')

#
# read_project90_data() - load the Project 90 data
#
# Paramters: 
#   datadir - directory containing the data
#
# Return value:
#    igraph object of hospital transfer network with attributes on nodes
#
read_project90_data <- function(project90_dir) {
  nodes <- read.table(paste(project90_dir, 'nodes.tsv',
                               sep=.Platform$file.sep), header=T)
                  
  edgelist <- read.table(paste(project90_dir, 'edges.tsv',
                               sep=.Platform$file.sep), header=T)

  g <- simplify(graph.edgelist(as.matrix(edgelist), directed=FALSE))
  stopifnot(vcount(g) == nrow(nodes))
  stopifnot(vcount(g) == 5492)
  stopifnot(ecount(g) == 43288/2) #each edge recorded twice but we simplified it
  V(g)$name <- as.integer(V(g)) # 'name' is special in igraph, lets us index directly
  # label graph node with attributes in id order
  # all are integer, although there are NA values
  for (aname in c('id', project90_attr_names)) {
    g <- set.vertex.attribute(g, aname, V(g)[order(V(g)$name)], nodes[ ,aname])
    stopifnot(V(g)$id == V(g)$name)
  }
  print(g)  #XXX
  return(g)
}

