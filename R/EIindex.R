##
## File:    EIindex.R
## Author:  Alex Stivala
## Created: September 2018
##

library(igraph)

##
## EIindex() - return E-I index of graph g on named categorical node attribute
##
## The E-I index is defined as (E - I) / (E + I)
##  where E is number of external links and I is number of internal links
##  where internal means same node category on both ends of link and
##  external is differing node category. Defined by
##
##    Krackhardt, D., & Stern, R. N. (1988). Informal networks and
##    organizational crises: An experimental simulation. Social
##    psychology quarterly, 123-140.
##
## Verified that this gets the same results as ei in the isnar package
## by Michal Bojanowski https://github.com/mbojan/isnar
## found via supplementary online material for
##
##   Cunningham, D., Everton, S., & Murphy, P. (2016). Understanding
##   dark networks: A strategic framework for the use of social network
##   analysis. Rowman & Littlefield.
##
## https://rpubs.com/pjmurphy/300606
##
## Paramters:
##    graph - igraph to get E-I index
##    attrname - name of categorical node attribute
##
## Return value:
##    E-I index of graph.
##
EIindex <- function(g, attrname) {
    ## get node attributes at both ends of all edges as adjacent values in vect
    vvect <- get.vertex.attribute(g, attrname, ends(g, E(g)))
    ## convert to matrix where each row has the adjacent node attributes as cols
    vmat <- matrix(vvect, ncol=2)
    ## so now simple to count same and different category pairs
    Ecount <- sum(vmat[,1] != vmat[,2])
    Icount <- sum(vmat[,1] == vmat[,2])
    stopifnot(Ecount + Icount == ecount(g))
    return( (Ecount - Icount) / (Ecount + Icount) )
}
