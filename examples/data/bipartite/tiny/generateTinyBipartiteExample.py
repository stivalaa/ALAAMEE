#!/usr/bin/Rscript
###
### File:    generateTinyBipartiteExample.py
### Author:  Alex Stivala
### Created: August 2022
###
### Generate tiny bipartite network and write bipartite network in Pajek
### format along with an outcome binary variable for ALAAM testing.
###
### Usage:
### 
### Rscript generateTinyBipartiteExample.py
###
### Output files (WARNING overwritten)
###    tiny_biparti   te.net       - network in Pajek format
###    tiny_biadjacency_matrix.txt - biadjacency matrix for MPNet
###    tiny_outcome.txt            - outcome binary variable
###    tiny.pdf                    - plot of network coloured by outcome var
###
### Note that the variables and their types to write to the output files
### are hardcoded in this script.
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




############################################################################
##                          Main
############################################################################



args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 0) {
  cat("Usage: generateTinyBipartiteExample.R\n")
  quit(save="no")
}


network_name <- 'tiny'

# Create bipartite graph
m <- 3
n <- 2
g <- make_bipartite_graph(types = c(rep(FALSE, m), rep(TRUE, n)),
                          edges = c(1,4, 1,5, 2,4, 2,5, 3,5, 3,4),
                          directed = FALSE)
stopifnot(vcount(g) == m + n)
 
##  binary outcome variable
V(g)$outcome <- c(0, 0, 0, 0, 1)

print(g)


##
## get biadjacency matrix
##

A <- as.matrix(get.adjacency(g))
print(A)
B <- A[1:m, (m+1):(m+n)]
print(B)
tB <- A[(m+1):(m+n), 1:m]
stopifnot(all(t(B) == tB))

##
## write graph
##

write.graph(g, paste(network_name, "_bipartite.net", sep=''),
                 format = "pajek")


##
## write biadjacency matrix
##

write.table(B, paste(network_name, "_biadjacency_matrix.txt", sep=''),
            row.names = FALSE, col.names = FALSE)
            
##
## write binary outcome attribute 
##
binattr <- data.frame(outcome = ifelse(is.na(V(g)$outcome), 0,
                                       ifelse(V(g)$outcome, 1, 0)))
write.table(binattr, file = paste(network_name, "outcome.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep='\t')


###
### write PDF file with network diagram
###
pdf('tiny.pdf')
plot(g, vertex.shape=ifelse(V(g)$type, "circle", "square"),
     vertex.color=V(g)$outcome, layout = layout.bipartite,
     vertex.label.family = "sans")
dev.off()
