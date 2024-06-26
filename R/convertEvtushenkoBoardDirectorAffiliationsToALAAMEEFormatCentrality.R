##!/usr/bin/Rscript
##
## File:    convertEvtushenkoBoardDirectorAffiliationsToALAAMEEFormatCentrality.R
## Author:  Alex Stivala
## Created: September 2022
##
## Read the network and attributes data in GML format for the 
## Evtushenko & Gastner (2019) company director network 
## and convert to Pajek bipartite format for ALAAMEE. 
## Also compute betweenness centrality and BiRank centrality measures
## for all the nodes.
## (Based on
## /convertEvtushenkoBoardDirectorAffiliationsToEstimNetDirectedFormat.R,
## in EstimNetDirected/scripts/,  but also write extra 'outcome' binary file for
## ALAAMEE and comptue centralities as conintuous attributes - not appropraite
## for ERGM as network is not fixed, but for ALAAM network is firxed.
##
## WARNING: betweenness centrality computation takes about 3 hours, so this
## script takes a long time to run.
##
## 
## Usage: Rscript convertEvtushenkoBoardDirectorAffiliationsToALAAMEEFormatCentrality.R [-g] board_director.gml.gz
## where board_director.gml.gz is the file downloaded from 
## https://zenodo.org/record/3553442
## (publication date November 26, 2019; downloaded 28 June 2020)
## If -g is specified then gets giant omponent of network.
##
## Output files in cwd (WARNING overwritten):
##     evtushenko_directors_bipartite.net
##     evtushenko_directors_binattr.txt
##     evtushenko_directors_catattr.txt
##     evtushenko_directors_contattr.txt
##     evtushenko_directors_outcome.txt
##     evtushenko_directors_outcome_na0.txt
##
## If -g (giant component) is specified, then filenames hae _gc appended before
## .txt suffix.
##
## Citation for publication of data:
##
##  A. Evtushenko and M. T. Gastner, Beyond Fortune 500: Women in a global
##  network of directors. In H. Cherifi et al. (Eds.), Complex Networks and 
##  Their Applications VIII, Proc. 8th Int. Conf. Complex Networks and Their 
##  Applications, Volume 1, pp. 586-598 (Springer, Cham, 2020), 
##  DOI: 10.1007/978-3-030-36683-4_47.
##
## Citation for data:
## 
##  Evtushenko, Anna, & Gastner, Michael T. (2019). Data set discussed in 
##  "Beyond Fortune 500: Women in a Global Network of Directors" (1.0)
##  [Data set]. 8th Int. Conf. Complex Networks and Their Applications
##  (COMPLEX NETWORKS 2019), Lisbon, Portugal. Zenodo.
##  https://doi.org/10.5281/zenodo.3553442
##
##
## From https://zenodo.org/record/3553442 :
##
##  Vertex attributes:
## 
##     id: unique identifier
##     type: "Person" or "Company"
##     age: years of age for vertices representing a person, "NA" if unknown for a person or if vertex represents a company
##     gender: "Male", "Female" or "NA" (unknown) if vertex represents a person, "NA" if vertex represents a company
##     country: name of country or "NA" (unknown) if vertex represents a company, "NA" if vertex represents a person
##     sector: segment of the economy in which a company operates. "NA" if vertex represents a person or if company's sector is unknown
##     industry: specific business (i.e. subset of sector) in which a company operates. "NA" if vertex represents a person or if company's industry is unknown.
##     employeesnum: number of company's employees. "NA" if vertex represents a person or if company's number of employees is unknown.
## 
##
## Citation for igraph is:
##   
##  Csardi G, Nepusz T (2006). .The igraph software package for complex
##   network research.. InterJournal, Complex Systems, 1695. https://igraph.org.
##
## Citations for BiRank and R package birankr to compute it are:
##
## He, X., Gao, M., Kan, M. Y., & Wang, D. (2016). Birank: Towards
## ranking on bipartite graphs. IEEE Transactions on Knowledge and
## Data Engineering, 29(1), 57-71.
##
## Yang, K. C., Aronson, B., & Ahn, Y. Y. (2020). BiRank: Fast and 
## flexible ranking on bipartite networks with R and python. 
## Journal of open source software, 5(51).
##

##
library(igraph)
library(reshape2) # for dcast to do "one-hot" binary coding of categorical vars
library(birankr)

##
## giant_component() - return largest connected component of the graph
## 
## Paramters:
##    graph - igraph to get giant componetn of
##
## Return value:
##    largest connected component of graph
##
giant.component <- function(graph) {
  cl <- clusters(graph)
  return(induced.subgraph(graph, which(cl$membership == which.max(cl$csize))))
}

###########################################################################
##
## main
##
###########################################################################

get_giantcomponent <- FALSE
args <- commandArgs(trailingOnly=TRUE)
if (length(args) < 1 || length(args) > 2 ||
    (length(args) == 2 && args[1] != "-g")) {
  cat("Usage: convertEvtushenkoBoardDirectorAffiliationsToALAAMEEFormatCentrality.R [-g] board_director.gml.gz\n")
  quit(save="no")
} else if (length(args) == 2) {
  get_giantcomponent <- TRUE
  infile <- args[2]
} else {
  infile <- args[1]
}

##
## network
##

cat("reading ", infile, "...\n")
system.time(g <- read.graph(gzfile(infile), format='gml'))

summary(g)

uniqueIds <- unique(V(g)$id)
numIds <- length(uniqueIds)
stopifnot(min(uniqueIds) == 0)
stopifnot(max(uniqueIds) == numIds-1)
stopifnot(length(V(g)$id) == numIds)

## remove multiple and self edges if any
g <- simplify(g , remove.multiple = TRUE, remove.loops = TRUE)
summary(g)


##
## make sure all Person nodes are first then all Company nodes
##
stopifnot(all(V(g)$type %in% c('Person', 'Company')))
num_Persons <- length(which(V(g)$type == 'Person'))
num_Companies <- length(which(V(g)$type == 'Company'))
cat('num_Persons = ', num_Persons, '\n')
cat('num_Companies = ', num_Companies, '\n')
stopifnot(num_Persons + num_Companies == vcount(g))
stopifnot(all(V(g)$type[1:num_Persons] == 'Person'))

##
## get giant component if specified
##
if (get_giantcomponent) {
  cat('getting giant component\n')
  g <- giant.component(g)
  summary(g)

  stopifnot(all(V(g)$type %in% c('Person', 'Company')))
  num_Persons <- length(which(V(g)$type == 'Person'))
  num_Companies <- length(which(V(g)$type == 'Company'))
  cat('num_Persons = ', num_Persons, '\n')
  cat('num_Companies = ', num_Companies, '\n')
  stopifnot(num_Persons + num_Companies == vcount(g))
  stopifnot(all(V(g)$type[1:num_Persons] == 'Person'))
}

##
## Replace spaces and '&' in strings with '.' and 'and' to
## prevent problems with header column names etc. (E.g. "Oil & gas" is 
## changed to "Oil.and.Gas"
## Also replace '-' with '.'
##

for (colname in c("sector", "industry", "country")) {
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub(" ", ".", s)))
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub("&", "and", s)))
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub("-", ".", s)))
}
## 
## get binary attributes
##

# 0 for Person, 1 for company (duplicates bipartite node type)
# also make a binary gender coded as 0 Male, 1 Female
binattr <- data.frame(company = ifelse(V(g)$type == 'Person', 0, 1),
                      female  = ifelse(V(g)$gender == 'Male', 0,
                                      ifelse(V(g)$gender == 'Female', 1, NA)))
summary(binattr)

##
## get categorical attributes
##
catattr <- data.frame(gender  = ifelse(V(g)$gender == "NA", NA, V(g)$gender),
                      country = ifelse(V(g)$country == "NA", NA, V(g)$country),
                      sector  = ifelse(V(g)$sector == "NA", NA, V(g)$sector),
                      industry= ifelse(V(g)$industry == "NA", NA, V(g)$industry))
## print the factor levels to stdout for future reference (codebook)
print("gender")
catattr$gender <- factor(catattr$gender)
print(levels(catattr$gender))
print("country")
catattr$country <- factor(catattr$country)
print(levels(catattr$country))
print("sector")
catattr$sector <- factor(catattr$sector)
print(levels(catattr$sector))
print("industry")
catattr$industry <- factor(catattr$industry)
print(levels(catattr$industry))


##
## make binary ("one-hot") version of gender and sector attributes,
## and add to binary attributes
##

catattr_recoded <- catattr
catattr_recoded$ID <- seq(1:nrow(catattr_recoded))
catattr_recoded <- dcast(data = melt(catattr_recoded, id.vars = "ID"),
                         ID ~ variable + value, fun.aggregate = length)
catattr_recoded$ID <- NULL
binattr <- cbind(binattr, catattr_recoded)

## One-hot encoding above with melt and dcast adds an _NA dummy variable,
## and has 0 for for values that were NA. Use the _NA dummy to recode
## all dummy variables that were for an NA value back to NA

for (colname in c("gender", "sector", "industry", "country")) {
  NA_idx <- which(binattr[, paste(colname, "NA", sep="_")] == 1)
  dummyvarnames <- Filter(function(s) substr(s, 1, nchar(colname)+1) == paste(colname, '_', sep='') && s != paste(colname, "NA", sep="_"), names(binattr))
  for (varname in dummyvarnames) {
    binattr[NA_idx, varname] <- NA
  }
}


## Have to replace '_' with '.' in column names as reshape2 melt/dcast above
## introduces '_' 
colnames(binattr) <- sapply(colnames(binattr), function(s) gsub("_", ".", s))

# compare auto encoding to original gender binary coding to check
stopifnot(all(is.na(catattr$gender) == as.logical(binattr$gender.NA)))
stopifnot(all(binattr$female == binattr$gender.Female, na.rm=TRUE))


##
## convert categorical attributes to integer values (as written to stdout above)
##
summary(catattr)
catattr$gender <- as.numeric(catattr$gender)
catattr$country <- as.numeric(catattr$country)
catattr$sector <- as.numeric(catattr$sector)
catattr$industry <- as.numeric(catattr$industry)
summary(catattr)
                       

##
## get continuous attributes
##

contattr <- data.frame(age = ifelse(V(g)$age == "NA", NA, as.numeric(V(g)$age)),
                     employeesnum = ifelse(V(g)$employeesnum == "NA", NA, as.numeric(V(g)$employeesnum)))


##
## compute BiRank centrality and add as continuous attribute
##

elist <- as.data.frame(get.edgelist(g))
names(elist) <- c("person", "company")
system.time( bprank <- bipartite_rank(data = elist,
                                      normalizer = "BiRank",
                                      return_mode= "both"))
contattr$birank <- c(bprank$rows$rank, bprank$columns$rank)

##
## compute betweeneess centrality and add as continuous attribute
## WARNNG: This takes about 3 hours
##

cat("Computing betweeneess centrality...\n")
system.time( contattr$betweenness <- betweenness(g, directed = FALSE, 
                                                    normalized = FALSE) )


##
## compute harmonic centrality and add as continuous attribute
## Harmonic centrality is mean inverse distance to all other vertices,
## considering unreachable to have zero inverse distance.
## This is a kind of closeness centrality, but is well-defined on
## unconnected graphs (not just connected graphs).
## Citation in igraph manual is Marchiori & Latora (2000) Physica A 285
## But see
## https://en.wikipedia.org/wiki/Centrality#Harmonic_centrality
## for long history of the same or similar idea
##

cat("Computing harmonic centrality...\n")
system.time(contattr$harmonic.cent <- harmonic_centrality(g, normalized=FALSE))


##
## scale and center the centrality measures so regression coefficients not
## huge (e.g. birank) or tiny (eg. betweenness)
##

contattr$birank.scaled        <- scale(contattr$birank, center = TRUE, scale = TRUE)
contattr$betweenness.scaled   <- scale(contattr$betweenness, center = TRUE, scale = TRUE)
contattr$harmonic.cent.scaled <- scale(contattr$harmonic.cent, center = TRUE, scale = TRUE)



summary(contattr)

##
## get outcome binary attribute
##
outcome <- data.frame(female = binattr$female)

## And version with NA values converted to 0 (on person nodes only)
outcome_na0 <- data.frame(female = ifelse(binattr$company, binattr$female,
                                          ifelse(is.na(binattr$female),
                                                 0, binattr$female)))


###
### convert type to logical so Pajek bipartite format output works
###
# have to do it this cumbersome way as if do not delete type attr it always
# remains character not logical
V(g)$ltype <- (V(g)$type == 'Company') # TRUE for company, FALSE for person
g <- remove.vertex.attribute(g, 'type')
V(g)$type <- V(g)$ltype
summary(g)
stopifnot(typeof(V(g)$type) == 'logical')
stopifnot(sum(V(g)$type) == num_Companies)

###
### write graph
###


outfilename <- 'evtushenko_directors_bipartite.net'
if (get_giantcomponent) {
  outfilename <- 'evtushenko_directors_bipartite_gc.net'
}
write.graph(g, outfilename, format="pajek")


##
## write binary attributes
##

write.table(binattr,
            file = ifelse(get_giantcomponent,
                          "evtushenko_directors_binattr_gc.txt", 
                          "evtushenko_directors_binattr.txt"),
            row.names = FALSE, col.names = TRUE, quote = FALSE)

##
## write categorical attributes
##

write.table(catattr,
            file = ifelse(get_giantcomponent,
                          "evtushenko_directors_catattr_gc.txt", 
                          "evtushenko_directors_catattr.txt"),
            row.names = FALSE, col.names = TRUE, quote=FALSE)

##
## write continuous attributes
##

write.table(contattr,
            file = ifelse(get_giantcomponent,
                          "evtushenko_directors_contattr_gc.txt", 
                          "evtushenko_directors_contattr.txt"),
            row.names = FALSE, col.names = TRUE, quote = FALSE)

##
## write outcome binary attribute
##

write.table(outcome,
            file = ifelse(get_giantcomponent,
                          "evtushenko_directors_outcome_gc.txt", 
                          "evtushenko_directors_outcome.txt"),
            row.names = FALSE, col.names = TRUE, quote = FALSE)

## and version with NA replaced with 0 for person nodes only

write.table(outcome_na0,
            file = ifelse(get_giantcomponent,
                          "evtushenko_directors_outcome_na0_gc.txt", 
                          "evtushenko_directors_outcome_na0.txt"),
            row.names = FALSE, col.names = TRUE, quote = FALSE)


## end
