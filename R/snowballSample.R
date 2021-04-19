#
# File:    snowballSample.R
# Author:  Alex Stivala
# Created: November 2013
#
# 
# Functions for
# snowball sampling in a (large) network, retaining zone information
# for each sampled node.
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

#
# giant_component() - return largest connected component of the graph
# 
# Paramters:
#    graph - igraph to get giant componetn of
#
# Return value:
#    largest connected component of graph
#
giant.component <- function(graph) {
  cl <- clusters(graph)
  return(induced.subgraph(graph, which(cl$membership == which.max(cl$csize))))
}

#
# snowball_sample() - snowball sampling
#
# Parameters:
#    g - graph to sample from( igraph)
#    num_waves - number of snowball waves (NB for cnostistney with SPNet
#                1 is subtraced so putting 3 here means there are really
#                only two waves [in normal usage] but there are 2 different
#                zones (0 for seeds, 1 wave first wave, 2 for 2nd wave)
#    seeds - vector of seeds (node ids) to start snowball sample from
#    max_num_links - (default Inf) maximum number of links to follow in
#                    sampling. If Inf (default) follows all edges from a node
#                    otherwise picks random set of edges from node v
#                    of size min(degree(v), max_num_links)
#
# Return value:
#    graph (igraph) snowball sampled from g with each node having 
#    a zone attribute for snowball sampling zone(0=seed, 1=first wave, etc.)
#

# All sorts of fancy things can be done in R with igraph e.g.:
#
# induced.subgraph(h, Reduce(union, neighborhood(h, waves_num, sample.int(vcount(h), num_seeds) )))
# 
# or (to get the zone numbers (waves) instead of spedifying on input as above):
#
# lapply(sample.int(vcount(g), size=num_seeds), function(r) {zones <- graph.bfs(h, root=r, order=F, rank=F, father=F,pred=F,succ=F,dist=T,unreachable=F)$dist; list(nodes=which(zones<=num_waves), zones=zones[which(zones<=num_waves)])} )
#
# but in the end it is actually easier to just explictly write the code
# explicitly as done here to get the zones for all nodes without running
# into problems wih having to do union of node numbers and working out what
# zone corresponds to which node etc. all of which becomes a problem with
# "neat" versions like above in comments.
#
snowball_sample <- function(g, num_waves, seeds, max_num_links=Inf) {
  V(g)$zone <- NA
  V(g)[seeds]$zone <- 0
  nodes <- seeds
  newnodes <- nodes
  for (i in 1:num_waves) {
    newnodes <- Reduce(union, lapply(newnodes, function(v) 
                         Filter(function(x) !(x %in% nodes),
                                as.numeric(sample(neighbors(g, v),
                                       min(degree(g, v), max_num_links))))))
    if (!is.null(newnodes)) {
        V(g)[newnodes]$zone <- i
        nodes <- union(nodes, newnodes)
    }
  }
  return(induced.subgraph(g, nodes))
}

#
# snowball_sample_from_digraph() - snowball sampling from directed graph
#
# Parameters:
#    g - graph to sample from( igraph)
#    num_waves - number of snowball waves (NB for cnostistney with SPNet
#                1 is subtraced so putting 3 here means there are really
#                only two waves [in normal usage] but there are 2 different
#                zones (0 for seeds, 1 wave first wave, 2 for 2nd wave)
#    seeds - vector of seeds (node ids) to start snowball sample from
#
# Return value:
#    graph (igraph) snowball sampled from g with each node having 
#    a zone attribute for snowball sampling zone(0=seed, 1=first wave, etc.)
#
# This version does 'snowball sampling' from a directed graph by
# pretending that all the edges are actually unidrected (i.e. we 'follow'
# edges regardless of their direction - if there is a node a in our sample
# and directed link b->a then b will be sampled as we regrad it in the
# neighbourhood of a here (ignoring the edge direction). Hence this is
# is not really 'snowball sampling' as the graph we are sampling on
# is not the same as the actual graph - it is transformed by ignoring
# the edge dirctions (or equivalently thinking of them all as going 'out'
# from our seeds and samples). We might call it 'dirty snowball sampling',
# perhaps.
# All we have to do to implement this is use as.undirected(g) instead of just g
# in the neighbors() function.

snowball_sample_from_digraph <- function(g, num_waves, seeds) {
  V(g)$zone <- NA
  V(g)[seeds]$zone <- 0
  nodes <- seeds
  newnodes <- nodes
  for (i in 1:num_waves) {
    newnodes <- Reduce(union, lapply(newnodes, function(v) 
                         Filter(function(x) !(x %in% nodes),
                                neighbors(as.undirected(g), v))))
    if (!is.null(newnodes)) {
        V(g)[newnodes]$zone <- i
        nodes <- union(nodes, newnodes)
    }
  }
  return(induced.subgraph(g, nodes))
}

