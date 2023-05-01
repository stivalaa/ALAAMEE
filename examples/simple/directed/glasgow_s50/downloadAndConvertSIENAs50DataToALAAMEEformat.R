##!/usr/bin/Rscript
##
## File:    downloadAndConvertSIENAs50DataToALAAMEEformat.R
## Author:  Alex Stivala
## Created: May 2023
##
## Download the excerpt of 50 girls from the "Teenage Friends and Lifestyle
## Study" data from the SIENA datasets and convert to format for use
## with ALAAMEE.
##
## Usage:
## 
## Rscript downloadAndConvertSIENAs50DataToALAAMEEformat.R
##
## Output files in cwd (WARNING overwritten):
##     s50-friendships-directed.net
##     s50-binattr.txt
##     s50-catattr.txt
##     s50-contattr.txt
##     s50-outcome.txt
##     s50-adjmatrix.txt [for MPNet]
##
## Note using TAB not space separtors in attribute files so they can
## also be used in MPNet.
##
## The outcome here is set to 1 for smoking (any value > 1 in the original
## coding which is 1 (non), 2 (occasional) and 3 (regular, 
## i.e. more than once per week)) otherwise 0.
##
## The references for this data (as per the documentation from the SIENA
## data page) are:
##
##  Michell, L., and A. Amos (1997). Girls, pecking order and smoking. Social Science and Medicine, 44, 1861 - 1869.
##    Pearson, M.A., and L. Michell. 2000. Smoke Rings: Social network analysis of friendship groups, smoking and drug-taking. Drugs: education, prevention and policy, 7, 21-37.
##    Pearson, M., and P. West. 2003. Drifting Smoke Rings: Social Network Analysis and Markov Processes in a Longitudinal Study of Friendship Groups and Risk-Taking. Connections, 25(2), 59-76.
##    Pearson, Michael, Steglich, Christian, and Snijders, Tom. Homophily and assimilation among sport-active adolescent substance users. Connections 27(1), 47-63. 2006.
##    Steglich, C.E.G., Snijders, T.A.B. and West, P. (2006), Applying SIENA: An illustrative analysis of the co-evolution of adolescents' friendship networks, taste in music, and alcohol consumption.
##    Methodology, 2, 48-56.
##    West, P. and Sweeting, H. (1995) Background Rationale and Design of the West of Scotland 11-16 Study. Working Paper No. 52. MRC Medical Sociology Unit Glasgow. 
##
## Some of this code is copied from the tutorial for the Bayesian ALAAM
## R implementation by Johan Koskinen from here:
## https://github.com/johankoskinen/ALAAM/blob/main/ALAAM%20tutorial.Rmd
## (see https://github.com/johankoskinen/ALAAM/)
##
## The reference for this is:
##   Koskinen, J., & Daraganova, G. (2022). Bayesian analysis of social influence. Journal of the Royal Statistical Society Series A. 185(4), 1855-1881. https://doi.org/10.1111/rssa.12844
##
## As per that example for Bayesian ALAAM, we use the outcome (smoke) at 
## second wave as the outcome variable, and the network and other 
## covariates from the first wave. 

library(igraph)

args <- commandArgs(trailingOnly=TRUE)
if (length(args) > 1) {
  cat("Usage: downloadAndConvertSIENAs50DataToALAAMEEformat.R\n")
  quit(save="no")
}

## This code from https://github.com/johankoskinen/ALAAM/blob/main/ALAAM%20tutorial.Rmd

# Download and read
temp <- tempfile()
download.file("https://www.stats.ox.ac.uk/~snijders/siena/s50_data.zip",temp)
adj <- read.table(unz(temp, "s50-network1.dat"))
sport <- read.table(unz(temp, "s50-sport.dat"))
smoke <- read.table(unz(temp, "s50-smoke.dat"))
alcohol <- read.table(unz(temp, "s50-alcohol.dat"))
drugs <- read.table(unz(temp, "s50-drugs.dat")) # added this
unlink(temp)

# Format the network and set smoke at the second wave as our outcome variable
n <- nrow(adj)
adj <- as.matrix(adj) # convert from data.frame to matrix
smoke <- smoke[,2] # use wave 2
smoke[smoke<2] <- 0 # set non-smoker to 0
smoke[smoke>0] <- 1 # set occasional and regular to 1

## End of code from https://github.com/johankoskinen/ALAAM/blob/main/ALAAM%20tutorial.Rmd

##
## Write network
##
g <- graph_from_adjacency_matrix(adj, mode="directed", diag=FALSE)
summary(g)
stopifnot(n == vcount(g))
stopifnot(n == 50)
write.graph(g, file = "s50-friendships-directed.net", format = "pajek")
write.table(as.matrix(get.adjacency(g)), 's50-friendships-adjmatrix.txt', row.names=F, col.names=F)

##
## write outcome binary attribute
##

outcomebinattr <- data.frame(smoke = smoke)
summary(outcomebinattr)
write.table(outcomebinattr, file = "s50-outcome.txt",
            row.names = FALSE, col.names = TRUE, quote = FALSE)


##
## write categorical attributes
##

catattr <- data.frame(
                      sport = sport[, 1], # Sport: 1 (not regular) and 2 (regular
                      alcohol = alcohol[, 1], # Alcohol: 1 (non), 2 (once or twice a year), 3 (once a month), 4 (once a week) and 5 (more than once a week)
                      drugs = drugs[, 1] # Cannabis use: 1 (non), 2 (tried once), 3 (occasional) and 4 (regular)
                     )
summary(catattr)
write.table(catattr, file = "s50-catattr.txt",
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep = '\t')

##
## write binary attributes
## these are just recoded categorical attributes
##

binattr <- data.frame(
                     sport = ifelse(catattr$sport == 2, 1, 0), # 1 for regular sport
                     alcohol = ifelse(catattr$alcohol > 2, 1, 0), # 1 for any alcohol at all (only 0 for "non")
                     drugs = ifelse(catattr$drugs > 1, 1, 0) # 1 for any cannabis use at all (only 0 for "non")
                    )
summary(binattr)
write.table(binattr, file = "s50-binattr.txt",
            row.names = FALSE, col.names = TRUE, quote = FALSE, sep = '\t')
##
## write continuous attributes
## these are just the categorical attributes
##

contattr <- data.frame(
                      sport = sport[, 1], # Sport: 1 (not regular) and 2 (regular
                      alcohol = alcohol[, 1], # Alcohol: 1 (non), 2 (once or twice a year), 3 (once a month), 4 (once a week) and 5 (more than once a week)
                      drugs = drugs[, 1] # Cannabis use: 1 (non), 2 (tried once), 3 (occasional) and 4 (regular)
                     )
summary(contattr)
write.table(contattr, file = "s50-contattr.txt",
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep = '\t')

