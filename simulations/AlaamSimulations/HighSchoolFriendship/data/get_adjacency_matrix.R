###
### File:    get_adjacency_matrix.R
### Author:  Alex Stivala
### Created: February 2022
###
### Load Pajek format arc list created by
### convert_highschoolfriendship_directed_network_to_pajek_ALAAMEE_format.R
### and write adjacency matrix (useful for MPNet)
###
### Output files in cwd (WARNING: overwrites if present):
###
###   highschool_friendship_adjmatrix.txt
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

g <- read.graph('highschool_friendship_arclist.net', format='pajek')
write.table(as.matrix(get.adjacency(g)), 'highschool_friendship_adjmatrix.txt', row.names=F, col.names=F)
