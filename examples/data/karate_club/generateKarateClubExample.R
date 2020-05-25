#!/usr/bin/Rscript
###
### File:    generateKarateClubExample.R
### Author:  Alex Stivala
### Created: July 2019
###
### Write the Zachary Karate Club network and actor attributes
### (binary, continuous, categorical) to files for MPNet ALAAM
### estimation.  The faction from the original data is used as the
### outcome variable.  The other variables are randomly generated.
###
### Usage:
### 
### Rscript generateKarateClubExample.R 
###
### Output files (WARNING overwritten)
###    karate_adjmatrix.txt       - adjacency matrix
###    karate_outcome.txt         - outcome binary variable (faction)
###    karate_binattr.txt         - continuous attributes
###    karate_catattr.txt         - categorical attributes
###    karate_contattr.txt        - continuous attributes
###    karate.pdf                 - plot of network coloured by faction
###
### Note that the variables and their types to write to the output files
### are hardcoded in this script.
###
### Karate club data citation:
###
###  Zachary, W. W. (1977). An information flow model for conflict and
###  fission in small groups. Journal of anthropological research,
###  33(4), 452-473.
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
library(igraphdata) ## contains the karate club data set



### 
### write_graph_file() - write adjacency matrix
###
### Parameters:
###     filename - filename to write to (warning: overwritten)
###     g - igrpah graph object
###     write_header - if TRUE write Pajek header lines
###
### Return value:
###    None
###
write_graph_file <- function(filename, g, write_header=TRUE) {
  f <- file(filename, open="wt")
  if (write_header) {
    cat('*vertices ', vcount(g), '\n', file=f)
    cat('*matrix\n', file=f)
  }
  write.table(get.adjacency(g, sparse=F), file=f, col.names=F, row.names=F)
  close(f)
}


############################################################################
##                          Main
############################################################################

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 0) {
  cat("Usage: generateKarateClubExample.R\n")
  quit(save="no")
}


data('karate')

network_name <- 'karate'
g <- karate

print(g)

###
### write PDF file with network diagram
###
pdf('karate.pdf')
plot(karate)
dev.off()

##
## generate random node attributes
##


## random binary node attributes
V(g)$senior <- sample(c(FALSE, TRUE), vcount(g), replace=TRUE)

## random categorical node attributes
V(g)$gender <- sample(0:2, vcount(g), replace=TRUE)
V(g)$class <- sample(0:9, vcount(g), replace=TRUE)

## random continuous node attributes
V(g)$age <- rnorm(mean = 33, sd = 10, n = vcount(g))
V(g)$value <- rnorm(mean = 5, sd = 3, n = vcount(g))

print(g)


##
## write graph
##

write_graph_file(paste(network_name, "_adjmatrix.txt", sep=''), g,
                 write_header = FALSE)

##
## write binary outcome attribute (faction is 1 or 2, convert to 0 or 1)
##
binattr <- data.frame(faction = ifelse(V(g)$Faction==2, 1, 0))
write.table(binattr, file = paste(network_name, "outcome.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep='\t')


##
## write binary attributes
##
binattr <- data.frame(senior = ifelse(V(g)$senior, 1, 0))
write.table(binattr, file = paste(network_name, "binattr.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep='\t')


##
## write categorical attributes
##

catattr <- data.frame(gender = V(g)$gender,
                      class = V(g)$class)
write.table(catattr, file = paste(network_name, "catattr.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep='\t')

##
## write continuous attributes
##
contattr <- data.frame(age = V(g)$age,
                       value = V(g)$value)
write.table(contattr, file = paste(network_name, "contattr.txt", sep="_"),
            row.names = FALSE, col.names = TRUE, quote = FALSE, sep='\t')

