###
### File:    convert_highschoolfriendship_directed_network_to_pajek_ALAAMEE_format.R
### Author:  Alex Stivala
### Created: February 2022
###
### Load the SocioPatterns high school friendship network.
### This is a directed network of reported friendships.
### Convert to Pajek arclist format and attribute files for ALAAMEE.
###
### Output files in cwd (WARNING: overwrites if present):
###
###   highschool_friendship_arclist.net
###   highschool_friendship_catattr.txt
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

source('load_highschoolfriendship_directed_network.R')

g <- load_highschoolfriendship_directed_network()

write.graph(g, 'highschool_friendship_arclist.net', format='pajek')
catattr <- data.frame(class = V(g)$class,
                      sex   = V(g)$sex)
catattr$class <- factor(catattr$class)
print(levels(catattr$class))
catattr$sex[which(catattr$sex == "Unknown")] <- NA
catattr$sex <- factor(catattr$sex)
print(levels(catattr$sex))
print(summary(catattr))
catattr$class <- as.numeric(catattr$class)
catattr$sex <- as.numeric(catattr$sex)
print(summary(catattr))
write.table(catattr, 'highschool_friendship_catattr.txt', sep='\t',
            row.names = FALSE, col.names = TRUE, quote=FALSE)

