###
### File:    load_highschoolfriendship_directed_network.R
### Author:  Alex Stivala
### Created: September 2019
###
### Load the SocioPatterns high school friendship network.
### This is a directed network of reported friendships.
### Returned as igraph object.
###
###
### Data source:
###
### http://www.sociopatterns.org/datasets/high-school-contact-and-friendship-networks/
###
### Citation for data:
###
###   Mastrandrea, R., Fournet, J., & Barrat, A. (2015). Contact patterns
###   in a high school: a comparison between data collected using
###   wearable sensors, contact diaries and friendship surveys. PloS
###   One, 10(9), e0136497.
###
###
###

library(igraph)

load_highschoolfriendship_directed_network <- function() {
  zelfile <- gzfile('Friendship-network_data_2013.csv.gz')
  el <- read.table(zelfile, header=F)
  el$V1 <- as.character(el$V1)
  el$V2 <- as.character(el$V2)
  g <- graph_from_edgelist(as.matrix(el))

  metadata <-read.table('metadata_2013.txt', header=F,stringsAsFactors=F)
  names(metadata) <- c('id','class','sex')

  metadata$id <- as.character(metadata$id)

  for (v in V(g)) {
    for (aname in c('class', 'sex') ) {
      g <- set.vertex.attribute(g, aname, v, metadata[which(metadata$id == V(g)[v]$name), aname])
    }
  }
  return(g)
}
