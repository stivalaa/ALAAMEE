##!/usr/bin/Rscript
##
## File:    convertSNAPhiggsTWitterToALAAMEEFormat.R
## Author:  Alex Stivala
## Created: August 2023
##
## Read the network and attributes data for the Higgs TWitter dataset
## from https://snap.stanford.edu/data/higgs-twitter.html
## and convert to Pajek format for ALAAMEE or EstimNetDirected.  See
## documentation in
## https://snap.stanford.edu/data/higgs-twitter.html
## and source citation:
##
## De Domenico, M., Lima, A., Mougel, P., & Musolesi, M. (2013). The
## anatomy of a scientific rumor. Scientific reports, 3(1), 2980.
##
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
##
## For Use as example for network autocorrelation or peer effects
## model (or similar) see:
##
## Bartal, A., Pliskin, N., & Ravid, G. (2019). Modeling influence on
## posting engagement in online social networks: Beyond neighborhood
## effects. Social Networks, 59, 61-76.
##
## Li, M., & Kang, E. L. (2019). Randomized algorithms of maximum
## likelihood estimation with spatial autoregressive models for
## large-scale networks. Statistics and Computing, 29, 1165-1179.
##
##
## Usage:
## 
## Rscript convertSNAPhiggsTWitterToALAAMEEFormat.R
##
## Reads files (download via links at
## https://snap.stanford.edu/data/higgs-twitter.html) in cwd:
##
##   higgs-social_network.edgelist.gz
##   higgs-retweet_network.edgelist.gz
##   higgs-reply_network.edgelist.gz
##   higgs-mention_network.edgelist.gz
##   higgs-activity_time.txt.gz
##
##
## Output files in cwd (WARNING overwritten):
##
##   higgs_social.net
##   higgs_mention.net
##   higgs_reply.net
##   higgs_retweet.net
##   higgs_mention_active.txt
##   higgs_retweet_active.txt
##   higgs_reply_active.txt
##

library(dplyr)
library(igraph)

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 0) {
  cat("Usage: convertSNAPhiggsTWitterToALAAMEEFormat.R\n")
  quit(save="no")
}

##
## Social network
##

## From https://snap.stanford.edu/data/higgs-twitter.html :
##  Social Network statistics
##  Nodes 	456626
##  Edges 	14855842
##  Nodes in largest WCC 	456290 (0.999)
##  Edges in largest WCC 	14855466 (1.000)
##  Nodes in largest SCC 	360210 (0.789)
##  Edges in largest SCC 	14102605 (0.949)
##  Average clustering coefficient 	0.1887
##  Number of triangles 	83023401
##  Fraction of closed triangles 	0.002901
##  Diameter (longest shortest path) 	9
##  90-percentile effective diameter 	3.7

social_edgelist <- read.table('higgs-social_network.edgelist.gz')
higgs_social <- graph_from_data_frame(social_edgelist, directed = TRUE)
summary(higgs_social)

##  Nodes 	456626
##  Edges 	14855842
stopifnot(vcount(higgs_social) == 456626)
stopifnot(ecount(higgs_social) == 14855842)

## remove multiple and self edges
higgs_social <- simplify(higgs_social,
                         remove.multiple = TRUE, remove.loops = TRUE)
summary(higgs_social)


##
## Write social network
##
write.graph(higgs_social, "higgs_social.net", format="pajek")



##
## Other networks (retweet, reply, mention)
##
retweet_edgelist <- read.table('higgs-retweet_network.edgelist.gz')
higgs_retweet <- graph_from_data_frame(retweet_edgelist, directed = TRUE)
higgs_retweet <- simplify(higgs_retweet)
write.graph(higgs_retweet, "higgs_rewtweet.net", format='pajek')

reply_edgelist <- read.table('higgs-reply_network.edgelist.gz')
higgs_reply <- graph_from_data_frame(reply_edgelist, directed = TRUE)
higgs_reply<-simplify(higgs_reply)
write.graph(higgs_reply, "higgs_reply.net", format='pajek')

mention_edgelist <- read.table('higgs-mention_network.edgelist.gz')
higgs_mention <- graph_from_data_frame(mention_edgelist, directed = TRUE)
higgs_mention<-simplify(higgs_mention)
write.graph(higgs_mention, "higgs_mention.net", format='pajek')

##
## Activity data
##
#(not used)
#higgs_activity <- read.table('higgs-activity_time.txt.gz')



##
## Get binary attribute for activity (i.e any count larger than zero)
## for retweet, reply, mention
##

g <- higgs_social

## Slow, but not nearly as slow as doing it directly on graph attributes:

reply_to_counts_df <- as.data.frame( reply_edgelist %>% group_by(V1) %>% summarize(sum = sum(V3)) )
reply_count_df <- data.frame(node = 1:vcount(g), reply_count = NA)
for (i in 1:nrow(reply_to_counts_df)) {
  #cat(i,  reply_to_counts_df[i, "V1"], " ")
  reply_count_df[which(reply_count_df$node == reply_to_counts_df[i, "V1"]), "reply_count"] <- reply_to_counts_df[i, "sum"]
}
reply_count_df[which(is.na(reply_count_df$reply_count)), "reply_count"] <- 0

V(g)$reply_count <- reply_count_df$reply_count
V(g)$reply_active <- V(g)$reply_count > 0
reply_active_df <- data.frame(reply_active = V(g)$reply_active)
V(g)$reply_active <- V(g)$reply_count > 0
reply_active_df <- data.frame(reply_active = as.integer(V(g)$reply_active))
write.table(reply_active_df, "higgs_reply_active.txt", row.names=F, col.names=T, quote=F)




retweet_to_counts_df <- as.data.frame( retweet_edgelist %>% group_by(V1) %>% summarize(sum = sum(V3)) )
retweet_count_df <- data.frame(node = 1:vcount(g), retweet_count = NA)
for (i in 1:nrow(retweet_to_counts_df)) {
  #cat(i,  retweet_to_counts_df[i, "V1"], " ")
  retweet_count_df[which(retweet_count_df$node == retweet_to_counts_df[i, "V1"]), "retweet_count"] <- retweet_to_counts_df[i, "sum"]
}
retweet_count_df[which(is.na(retweet_count_df$retweet_count)), "retweet_count"] <- 0

V(g)$retweet_count <- retweet_count_df$retweet_count
V(g)$retweet_active <- V(g)$retweet_count > 0
retweet_active_df <- data.frame(retweet_active = as.integer(V(g)$retweet_active))
write.table(retweet_active_df, "higgs_retweet_active.txt", row.names=F, col.names=T, quote=F)



mention_to_counts_df <- as.data.frame( mention_edgelist %>% group_by(V1) %>% summarize(sum = sum(V3)) )
mention_count_df <- data.frame(node = 1:vcount(g), mention_count = NA)
for (i in 1:nrow(mention_to_counts_df)) {
  #cat(i,  mention_to_counts_df[i, "V1"], " ")
  mention_count_df[which(mention_count_df$node == mention_to_counts_df[i, "V1"]), "mention_count"] <- mention_to_counts_df[i, "sum"]
}
mention_count_df[which(is.na(mention_count_df$mention_count)), "mention_count"] <- 0

V(g)$mention_count <- mention_count_df$mention_count
V(g)$mention_active <- V(g)$mention_count > 0
mention_active_df <- data.frame(mention_active = as.integer(V(g)$mention_active))
write.table(mention_active_df, "higgs_mention_active.txt", row.names=F, col.names=T, quote=F)

