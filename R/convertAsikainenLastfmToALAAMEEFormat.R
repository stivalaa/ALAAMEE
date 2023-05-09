##
## File:    convertAsikainenLastfmToALAAMEEFormat.R
## Author:  Alex Stivala
## Created: May 2023
##
## Read the network and attributes data for the Last.fm data from:
##
##   Asikainen, A., Iñiguez, G., Ureña-Carrión, J., Kaski, K., &
##   Kivelä, M. (2020). Cumulative effects of triadic closure and
##   homophily in social networks. Science Advances, 6(19), eaax7310.
##
##   downloaded from:
##
##   https://zenodo.org/record/3726824
##
##   (DOI: 10.5281/zenodo.3726824)
##   Cite as:
##
##   Mikko Kivelä. (2020). The "Last.fm" data set used in the article
##   "Cumulative effects of triadic closure and homophily in social
##   networks" [Data
##   set]. Zenodo. https://doi.org/10.5281/zenodo.3726824
##
##
## and convert to Pajek format for ALAAMEE or EstimNetDirected.
##
##
## Usage:
## 
## Rscript convertAsikainenLastfmToALAAMEEFormat.R 
##
## Input files (in cwd):
##    lastfm.edg
##    lastfm_genders.txt
##
## Output files in cwd (WARNING overwritten):
##     lastfm.net
##     lastfm_binattr.txt
##
##
## As per the data description:
##
## lastfm.edg
##
## This is the network formatted as an edge list, where each row in
## the �le is an edge connecting the two nodes indicated by the two
## numbers separated by a whitespace. Each node number corresponds to
## a single account in the website.
##
## lastfm_genders.txt
##
## This is the list of genders of the nodes. Each row corresponds to
## one node. The �rst number is the node id (matching the one in the
## edge list) and the second number indicates the gender such that
## 0=male and 1=female.
##

library(igraph)

args <- commandArgs(trailingOnly=TRUE)
if (length(args) > 1) {
  cat("Usage: convertAsikainenLastfmToALAAMEEFormat.R\n")
  quit(save="no")
}
maxdegree_specified <- FALSE
if (length(args) == 1) {
    maxdegree_specified <- TRUE
    maxdegree <- as.integer(args[1])
}


##
## network
##
infile <- "lastfm.edg"
outfilename_undirected <- "lastfm.net"

cat("reading ", infile, "...\n")
system.time(edgelist <- read.table(infile))

uniqueIds <- unique(c(edgelist$V1, edgelist$V2))
numIds <- length(uniqueIds)
cat('number of unique ids is ', numIds, '\n')
cat('min is ', min(uniqueIds), ' max is ', max(uniqueIds), '\n')

uniqueIds <- unique(c(edgelist$V1, edgelist$V2))
numIds <- length(uniqueIds)
stopifnot(min(uniqueIds) == 0)
stopifnot(max(uniqueIds) == numIds - 1)


## have to add 1 as igraph cannot handle 0 as vertex id apparently
g <- graph.edgelist(as.matrix(edgelist)+1, directed=FALSE)


summary(g)
## remove multiple and self edges, if any
g <- simplify(g , remove.multiple = TRUE, remove.loops = TRUE)
summary(g)


##
## read attributes
##

gender <- read.table('lastfm_genders.txt')
names(gender) <- c('nodeid', 'female') 

## Make sure it really does line up with the node ids 1..N
stopifnot(nrow(gender) == numIds)
stopifnot(min(gender$nodeid) == 0)
stopifnot(max(gender$nodeid) == numIds - 1)



##
## get binary attributes
##
binattr <- data.frame(female = gender[, "female"]) # bool, 1 - female


##
## Write network
##
write.graph(g, outfilename_undirected, format="pajek")


##
## write binary attributes
##

summary(binattr)
write.table(binattr, file = "lastfm_binattr.txt",
            row.names = FALSE, col.names = TRUE, quote = FALSE)
