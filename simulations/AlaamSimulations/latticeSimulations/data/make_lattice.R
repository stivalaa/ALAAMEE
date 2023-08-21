#!/usr/bin/env Rscript
##
## File:    make_lattice.R
## Author:  Alex Stivala
## Created: August 2023
##
## Make lattice (two dimensional) network in Pajek format.
##

library(igraph)

g <- make_lattice(length = 100, dim = 2, directed= FALSE, circular = FALSE)
summary(g)
write_graph(g, file = "lattice.net", format='Pajek')
