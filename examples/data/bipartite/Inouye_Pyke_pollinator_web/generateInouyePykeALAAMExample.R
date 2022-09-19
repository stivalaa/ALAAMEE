#!/usr/bin/Rscript
###
### File:    generateInouyePykeALAAMExample.R
### Author:  Alex Stivala
### Created: August 2022
###
### Write actor attributes(binary, continuous, categorical) for Inouye-Pyke pollinator network
### to files for MPNet ALAAMestimation. The variables are randomly generated.
### Also write bipartite network in Pajek format.
###
### Usage:
### 
### Rscript generateInouyePykeALAAMExample.R 
###
### Output files (WARNING overwritten)
###    inouye_bipartite.net       - network in Pajek format
###    inouye_outcome.txt         - outcome binary variable
###    inouye_binattr.txt         - continuous attributes
###    inouye_catattr.txt         - categorical attributes
###    inouye_contattr.txt        - continuous attributes
###    inouye.pdf                 - plot of network coloured by outcome variable
###
### Note that the variables and their types to write to the output files
### are hardcoded in this script.
###
### Network data citation:
###
###   Inouye, D. W., and G. H. Pyke. 1988. Pollination biology in the Snowy Mountains of Australia: 
###   comparisons with montane Colorado, USA. Australian Journal of Ecology 13:191-210.
###
### igraph citations:
###
###  Gabor Csardi (2015). igraphdata: A Collection of Network Data Sets
###  for the 'igraph' Package. R package version 1.0.1.
###  https://CRAN.R-project.org/package=igraphdata
###
###  Csardi G, Nepusz T: The igraph software package for complex network
###  research, InterJournal, Complex Systems 1695. 2006. http://igraph.org
###

library(igraph)


#
# read_graph_matrix_file() - read adjacency matrix in paralle spnet format
#
# Parameters:
#     filename - filename of subgraph file to read from
#     directed - TRUE for directed graph
#
# Return value:
#     igraph graph object built from adjacency matrix
#
read_graph_matrix_file <- function(filename, directed) {
  # skip all lines that do not start with 0 or 1
  # this includes the first two lines *vertices n and *matrix as well as
  # all lines following the actual matrix with various stats etc.
  # which SPnet writes there (but not snowballSample.R)
  alltext <- readLines(filename)
  matrixtext <- grep("^[01][01 ]+$", alltext, value=T)
  adjmatrix <- as.matrix(read.table(textConnection(matrixtext)))
  if (directed) {
      g <- graph.adjacency(adjmatrix, mode='directed')
  } else {
      g <- graph.adjacency(adjmatrix, mode='undirected')
  }
  return(g)
}



############################################################################
##                          Main
############################################################################

set.seed(123)


args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 0) {
  cat("Usage: generateInouyePykeALAAMExample.R\n")
  quit(save="no")
}


network_name <- 'inouye'

# read biadjacency matrix 
B <- as.matrix(read.table('inouye_matrix.txt', header=F))
m = dim(B)[1]
n = dim(B)[2]

cat('m = ', m, '\n')
cat('n = ', n, '\n')

# Convert biadjacency matrix to adjacency matrix
A <- rbind(cbind(matrix(0, m, m), B), cbind(t(B), matrix(0, n,n)))
g <- graph_from_adjacency_matrix(A, mode='undirected')
V(g)[1:m]$type <- FALSE
V(g)[(m+1):(m+n)]$type <- TRUE

summary(g)
summary(degree(g, V(g)[which(V(g)$type == FALSE)]))
summary(degree(g, V(g)[which(V(g)$type == TRUE)]))


print(g)


##
## generate random node attributes
##



## random binary outcome variable
V(g)$outcome <- NA
V(g)$outcome[1:m] <- sample(c(FALSE, TRUE), m, replace=TRUE)

## random binary node attributes
V(g)$binattr <- sample(c(FALSE, TRUE), vcount(g), replace=TRUE)


## random categorical node attributes
V(g)$catattr <- sample(0:2, vcount(g), replace=TRUE)

## random continuous node attributes
V(g)$conattr <- rnorm(mean = 5, sd = 3, n = vcount(g))

print(g)


##
## write graph
##

write.graph(g, paste(network_name, "_bipartite.net", sep=''),
                 format = "pajek")

##
## write binary outcome attribute 
##
binattr <- data.frame(outcome = ifelse(is.na(V(g)$outcome), 0,
                                       ifelse(V(g)$outcome, 1, 0)))
#binattr <- data.frame(outcome = ifelse(V(g)[which(V(g)$type == FALSE)]$outcome, 1, 0))
write.table(binattr, file = paste(network_name, "outcome.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep='\t')

## version with NA not zero for mode B nodes
binattr <- data.frame(outcome = ifelse(is.na(V(g)$outcome), NA,
                                       ifelse(V(g)$outcome, 1, 0)))
write.table(binattr, file = paste(network_name, "outcome_BNA.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep='\t')



##
## write binary attributes
##
binattr <- data.frame(binattr = ifelse(V(g)$binattr, 1, 0))
write.table(binattr, file = paste(network_name, "binattr.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep='\t')


##
## write categorical attributes
##

catattr <- data.frame(catattr = V(g)$catattr)
write.table(catattr, file = paste(network_name, "catattr.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep='\t')

##
## write continuous attributes
##
contattr <- data.frame(conattr = V(g)$conattr)
write.table(contattr, file = paste(network_name, "contattr.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote = FALSE, sep='\t')



###
### write PDF file with network diagram
###
pdf('inouye.pdf')
plot(g, layout=layout.auto, vertex.shape=ifelse(V(g)$type, "circle", "square"),
     vertex.color=V(g)$outcome, vertex.label=NA, vertex.size=4)
dev.off()
