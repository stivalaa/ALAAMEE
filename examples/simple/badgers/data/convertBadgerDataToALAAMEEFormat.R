#!/usr/bin/Rscript
##
## File:    convertBadgerDataToALAAMEEFormat.R
## Author:  Alex Stivala
## Created: October 2023
##
## Read the badger data downloaded from the Supplementary Information of:
##
##   Silk, M. J., Croft, D. P., Delahay, R. J., Hodgson, D. J.,
##   Weber, N., Boots, M., & McDonald, R. A. (2017). 
##   The application of statistical network models in disease research. 
##   Methods in Ecology and Evolution, 8(9), 1026-1041.
##
## and convert to format for use with ALAAMEE.
## See Supplementary Information (Microsoft Word document 
## "Statistical network models and disease - supplementary materials.docx"
## in the zip file mee312770-sup-0001-supinfo.zip for more information
## on  the data and the R code used to extract it and use it in
## network autocorrelation, ERGM, and SAOM (but not ALAAM) models 
## described in the Silk et al. (2017) paper.
##
## Usage:
## 
## Rscript convertBadgerDataToALAAMEEFormat.R
##
## Reads file mee312770-sup-0001-supinfo.zip in cwd
##
## Output files in cwd (WARNING overwritten):
##     badgers_overallnetwork.net
##     badgers_TBpos.txt
##     badgers_binattr.txt
##     badgers_catattr.txt
##     badgers_contattr.txt
##

library(igraph)
library(sna)

infile <- 'mee312770-sup-0001-supinfo.zip'

## Build graph from overall adjacency matrix (undirected)
## The weighted adjacency matrix is converted to binary
X <- read.csv(unz(infile, 'overallnetwork.csv'))
xnames <- X[,1]
X <- as.matrix(X[,2:ncol(X)])
colnames(X) <- rownames(X) <- xnames
diag(X) <- NA
Xbinary <- ifelse(X > 0, 1, 0)
g <- graph_from_adjacency_matrix(Xbinary, mode='undirected',
                                 weighted=NULL, diag=FALSE)

## log edge weights in original adjacency matrix (used later for centrality)
X <- ifelse(X == 0, 0, log(X))

## Read bTB status and convert "N" and "P" to 0 and 1
TB <- read.csv(unz(infile, "TBstatsF.csv"))
stopifnot(all(TB$TBend %in% c("N", "P")))
stopifnot(all(TB$Badger == V(g)$name))
TB$TBstatus <- ifelse(TB$TBend == "P", 1, 0)

## Read ages, these are "Yearling" and "Adult"
Ages <- read.csv(unz(infile, "Ages.csv"))
stopifnot(all(Ages$ID == V(g)$name))

## Read sexes, these are "M" and "F"
Sex <- read.csv(unz(infile, "indivsexes.csv"))
stopifnot(all(Sex$ID == V(g)$name))

## Read in social group membership
groups <- read.csv(unz(infile, "Complete Membership.csv"))
stopifnot(all(groups$ID == V(g)$name))
