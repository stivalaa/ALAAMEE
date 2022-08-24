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
###    tiny_bipartite.net       - network in Pajek format
###    tiny_outcome.txt         - outcome binary variable
###    tiny.pdf                 - plot of network coloured by outcome variable
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
g <- make_bipartite_graph(types = c(FALSE, FALSE, FALSE, TRUE, TRUE),
                          edges = c(1,4, 1,5, 2,4, 2,5, 3,5, 3,4),
                          directed = FALSE)

 
##  binary outcome variable
V(g)$outcome <- c(0, 0, 0, 0, 1)

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
