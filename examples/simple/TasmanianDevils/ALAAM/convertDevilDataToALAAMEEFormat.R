#!/usr/bin/env Rscript
##
## File:    convertDevilDataToALAAMEEFormat.R
## Author:  Alex Stivala
## Created: October 2023
##
## Read data from:
##
##   Hamilton, D. G., Jones, M. E., Cameron, E. Z., Kerlin, D. H.,
##   McCallum, H., Storfer, A., ... & Hamede, R. K. (2020). Infectious
##   disease and sickness behaviour: tumour progression affects
##   interaction patterns and social network structure in wild
##   Tasmanian devils. Proceedings of the Royal Society B, 287(1940),
##   20202454.
##
## using the replication data (in ../data/ directory) from dryad repository
## https://dx.doi.org/10.5061/dryad.xksn02vdp
##
##
## and convert to format for ALAAM estimation with ALAAMEE software.
## The data has networks and wounds, tumours, and DFTD status (which is
## just 1 for any tumours else 0) for 12 (fortnightly) time periods. For
## ALAAM here we aggregate the network over the entire 12 periods
## (by just summing the adjacency matrices, which are converted to binary
## by ../SAOM/load_data.R whic is taken from the Hamilton et al. (2020)
## TERGM replicaion code, used for TERGMs in that paper, and also for my
## SAOM models in ../SAOM) and then converting to binary.
##
## The new wounds count data is aggregated by summing the rows (i.e. wound count
## for each individual is sum of all the new wound counts across time).
## The DFTD status binary variable is taken as the value at the last time 
## period (note that tumour load factor and hence DFTD status 
## in nondecreasing across time).
##
## Sex binary attribute is coded as 0 for female and 1 for male.
## It is also coded as a categorical attribute the same way (this allows
## for matching sex, not just activity/interaction for male).
##
## As well as the entire time period (12 fortnights), we also output
## data for the mating period (5 fortnights, f3 - f7) and the
## subsequent non-mating period (5 fortnights, f8 - 12). (Note that,
## unlike the TERGM replication code, we use only f8 - f12 for the
## non-mating period, rather than f1 - f2 and f8 - 12. In this way the
## non-mating period is contiguous rather than interrupted by the
## mating period, and also of the same duration; the data for f1 and
## f2 is then not used, however).
##
## Output files in cwd (WARNING: overwrites):
##   devils_contact_all.net
##   devils_DFTD_status_all.txt
##   devils_binattr_all.txt
##   devils_contattr_all.txt
##   devils_contact_mating.net
##   devils_DFTD_status_mating.txt
##   devils_binattr_mating.txt
##   devils_contattr_nonmating.txt
##   devils_contact_nonmating.net
##   devils_DFTD_status_nonmating.txt
##   devils_binattr_nonmating.txt
##   devils_contattr_nonmating.txt
##
## 
## Data not being used here is tumour load factor (DFTD status is just
## the binary version of this continuous variable).
##

library(igraph)

sessionInfo()

source('../SAOM/load_data.R')

##
## put contact adjacency matrices into array of time periods
##
contactData <- array(c(as.matrix(f1),as.matrix(f2),as.matrix(f3),as.matrix(f4),as.matrix(f5),as.matrix(f6),as.matrix(f7),as.matrix(f8),as.matrix(f9),as.matrix(f10),as.matrix(f11),as.matrix(f12)), dim = c(22, 22, 12))

for (i in 1:dim(contactData)[3]) {
  stopifnot(all(dim(contactData[,,i] == c(22, 22))))
  stopifnot(all(rownames(contactData[,,i]) == colnames(contactData[,,i])))
  stopifnot(all(t(contactData[,,i]) == contactData[,,i])) #symmetric
}


###
### Convert and write the data for time period specified by start and end
### The suffix is put on the filenames
###
write_devils_data <- function(start, end, suffix) {

  contact_sum <- contactData[,,start]
  ## Can't work out how to do this easiy in R without loop; sum() does not work
  for (i in (start+1):end) {
    contact_sum = contact_sum + contactData[,,i]
  }

  g <- graph_from_adjacency_matrix(sign(contact_sum), mode = "undirected",
                                   weighted = NULL, diag = FALSE)
  summary(g)
  g <- simplify(g)
  summary(g)

  stopifnot(all(DFTD[,"ID"] == rownames(contact_sum)))
  stopifnot(all(Tumour[,"ID"] == rownames(contact_sum)))
  stopifnot(all(Sex[,"ID"] == rownames(contact_sum)))

  ## The DFTD status binary variable is taken as the value at the last time 
  ## period (note that tumour load factor and hence DFTD status 
  ## in nondecreasing across time).
  DFTD_status_end <- DFTD[,1+end] # add 1 as column 1 is ID

  ## The new wounds count data is aggregated by summing the rows
  ## (i.e. wound count for each individual is sum of all the new wound
  ## counts across time).
  Wounds_end <- rowSums(Wounds[,(1+start):(1+end)]) # add 1 as column 1 is ID

  ## Write network
  write.graph(g, file=paste(paste("devils_contact", suffix, sep="_"),
                            "net", sep="."), format="pajek")

  ## Write outcome binary attribute (DFTD status)
  outcomebinattr <- data.frame(DFTD_status = DFTD_status_end)
  summary(outcomebinattr)
  write.table(outcomebinattr, file = paste(paste("devils_DFTD_status", suffix,
                                                 sep="_"), "txt", sep="."),
              row.names = FALSE, col.names = TRUE, quote = FALSE)

  ## Write binary attributes
  binattr <- data.frame(male = Sex$Sex)  # 0 = female, 1 = male
  write.table(binattr, file = paste(paste("devils_binattr", suffix, sep="_"),
                                    "txt", sep="."),
              row.names = FALSE, col.names = TRUE, quote = FALSE)

  ## Write categorical attributes
  catattr <- data.frame(sex = Sex$Sex) # 0 = female, 1 = male
  summary(catattr)
  write.table(catattr, file = paste(paste("devils_catattr", suffix, sep="_"),
                                    "txt", sep="."),
              row.names = FALSE, col.names = TRUE, quote = FALSE)

  ## Compute centralites and clustering and write as continuous attributes
  degree_cent <- degree(g)
  betweenness_cent <- betweenness(g)
  closeness_cent <- closeness(g)
  clustering_coef <- transitivity(g, type = "local", isolates = "zero")

  ## Center and scale the centrality and clustering measures
  degree_cent <- scale(degree_cent, center = TRUE, scale = TRUE)
  betweenness_cent <- scale(betweenness_cent, center = TRUE, scale = TRUE)
  closeness_cent <- scale(closeness_cent, center = TRUE, scale = TRUE)
  clustering_coef <- scale(clustering_coef, center = TRUE, scale = TRUE)

  contattr <- data.frame(wounds = Wounds_end,
                         degree_cent = degree_cent,
                         betweenness_cent = betweenness_cent,
                         closeness_cent = closeness_cent,
                         clustering_coef = clustering_coef)
  summary(contattr)

  print(cor(contattr))
  ## Note very high correlations (> 0.9) between betweenness, closeness, degree
  ## (and correlation between closeness and degree centralities is  > 0.99)
  ## Also large negative correlations (< -0.75) between clustering coef. and
  ## all three centrality measures.

  write.table(contattr, file = paste(paste("devils_contattr", suffix, sep="_"),
                                    "txt", sep="."),
              row.names = FALSE, col.names = TRUE, quote = FALSE)


}


###
### Main
###


cat("=============================== all ================================\n")
write_devils_data(1, 12, "all")
cat("============================= mating period ========================\n")
write_devils_data(3, 7, "mating")
cat("=========================== nonmating period ========================\n")
write_devils_data(8, 12, "nonmating")
