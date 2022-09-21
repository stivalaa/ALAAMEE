##!/usr/bin/Rscript
##
## File:    convertConnect4BoardDirectorAffiliationsToALAAMEEFormatCentrality.R
## Author:  Alex Stivala
## Created: September 2022
##
## Read the network and attributes data in CSV format for the 
## Connect4 & Gastner (2019) company director network 
## and convert to Pajek bipartite format for ALAAMEE or EstimNetDirected.
## Also compute betweenness centrality and BiRank centrality measures
## for all the nodes.
##
## Usage: Rscript convertConnect4BoardDirectorAffiliationsToALAAMEEFormatCentrality.R [-g] search.csv
##
## where search.csv is the query result from selecting all companies and
## all directors from the Connect 4 Boardroom database.
## Accessed from Swinburne at https://www-connect4-com-au.eu1.proxy.openathens.net/cms/boardroom/index.html
## (14 September 2022 by Peng at Swinburne).
## The Connect 4 Boardroom database ia a Thomson Reuters commercial
## prodct:
## https://legal.thomsonreuters.com.au/products/connect4/boardroom.aspx
##
##
## If -g is specified then gets giant omponent of network.
##
## Output files in cwd (WARNING overwritten):
##     connect4_directors_bipartite.net
##     connect4_directors_binattr.txt
##     connect4_directors_catattr.txt
##     connect4_directors_contattr.txt
##     connect4_directors_outcome.txt
##     connect4_directors_nodeid.txt
##
## If -g (giant component) is specified, then filenames hae _gc appended before
## .txt suffix.
##
##
## Citation for igraph is:
##   
##   Csardi G, Nepusz T (2006). .The igraph software package for complex
##   network research.. InterJournal, Complex Systems, 1695. https://igraph.org.
##
## Citations for BiRank and R package birankr to compute it are:
##
##   He, X., Gao, M., Kan, M. Y., & Wang, D. (2016). Birank: Towards
##   ranking on bipartite graphs. IEEE Transactions on Knowledge and
##   Data Engineering, 29(1), 57-71.
##
##   Yang, K. C., Aronson, B., & Ahn, Y. Y. (2020). BiRank: Fast and 
##   flexible ranking on bipartite networks with R and python. 
##   Journal of open source software, 5(51).
##
## 
## Note: needs igraph version higher than 1.2.11 to allow named nodes and 
## types in make_bipartite_graph() (aka graph.bipartite()).
## Written using version 1.3.4.
## Also need R version 3.2.0 or later for trimws().
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
  cat("Usage: convertConnect4BoardDirectorAffiliationsToALAAMEEFormatCentrality.R [-g] search.csv\n")
  quit(save="no")
} else if (length(args) == 2) {
  get_giantcomponent <- TRUE
  infile <- args[2]
} else {
  infile <- args[1]
}

##
## Read Connect 4 Boardroom data and build director affiliation network
##

## the data from the search query look like this:
#"Connect 4 Boardroom Search Result:"
#"Include Delisted Companies, For year(s): Current, show Directors/Executives"
#
#"Year","Code","Company","Delisted Date","Surname","First Name","Middle Name","Known As","P-ID","Person","Gender","Age","Dec.","Country","Indep.","Nom.","Interim","Position","Appointed","Ceased"
#"Current","14D","1414 Degrees Ltd","","Evans","Alison","M","","40032","","F","0","","Australia","Y","","","Non Executive Director","01/05/2022",""
#
# So note we skip the first three lines and the fourth line is the header

cat("reading ", infile, "...\n")
system.time( dat <- read.csv(infile, skip=3, 
                             header=TRUE, stringsAsFactors=FALSE) )

## Create PersonID and CompanyID by prepending "Person" to P.ID
## and "Company" to company Code respectively, as there is one company
## code that is also a P.ID.
dat$PersonID <- paste("Person", dat$P.ID, sep='.')
dat$CompanyID <- paste("Company", dat$Code, sep='.')

## Make logical node_types vector for make_bipartite_graph().
## It is a named vector where the names are the node names used
## in construting the bipartite graph.
## We will put all the persons (FALSE) first, followed by all the 
## companies (TRUE).
## Note: needs igraph version higher than 1.2.11 to allow named nodes and 
## types in make_bipartite_graph() (aka graph.bipartite()).
## Written using version 1.3.4.
## Bipartite network node attribute type is FALSE for persons (directors)
## and TRUE for companies (boards).
num_Persons <- length(unique(dat$PersonID))
num_Companies <- length(unique(dat$CompanyID))
node_types <- c(rep(FALSE, num_Persons), rep(TRUE, num_Companies))
names(node_types) <- c(unique(dat$PersonID), unique(dat$CompanyID))

## Now make the edges vector in the correct format for make_bipartite_graph()
## I.e.:
##  "A vector defining the edges, the first edge points from the first 
##   element to the second, the second edge from the third to the fourth, etc.
##   For a numeric vector, these are interpreted as internal vertex ids. 
##   For character vectors, they are interpreted as vertex names. "
## [https://search.r-project.org/CRAN/refmans/igraph/html/make_graph.html]
##
## For the transpose and concatenate method to convert the two column
## edge list to this format, see
## https://stackoverflow.com/questions/41051823/convert-a-two-column-matrix-into-a-comma-separated-vector
##
gedges <- c(t(as.matrix(dat[,c("PersonID", "CompanyID")])))

cat('num_Persons = ', num_Persons, '\n')
cat('num_Companies = ', num_Companies, '\n')

## make the bipartite graph
g <- graph.bipartite(types = node_types, edges = gedges, directed = FALSE)
summary(g)

stopifnot(typeof(V(g)$type) == 'logical')
stopifnot(sum(V(g)$type) == num_Companies)
stopifnot(num_Persons + num_Companies == vcount(g))
stopifnot(all(V(g)$type[1:num_Persons] == FALSE))
stopifnot(all(V(g)$type[(1+num_Persons):vcount(g)] == TRUE))

## add node attributes
print('adding node attributes to graph...')
for (colname in names(dat)) {
  g <- set.vertex.attribute(g, colname, value = dat[, colname])
}
summary(g)

## remove multiple and self edges if any
print('removing multiple and self edges...')
g <- simplify(g , remove.multiple = TRUE, remove.loops = TRUE)
summary(g)



##
## get giant component if specified
##
if (get_giantcomponent) {
  cat('getting giant component\n')
  g <- giant.component(g)
  summary(g)

}

##
## Replace spaces and '&' in strings with '.' and 'and' to
## prevent problems with header column names etc. (E.g. "Oil & gas" is 
## changed to "Oil.and.Gas"
## Also replace '-' with '.' and '/' with '.'
##
print('replacing problematic characters in strings with "."...')
for (colname in names(dat)) {
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub(" ", ".", s)))
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub("&", "and", s)))
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub("-", ".", s)))
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub("/", ".", s)))
}


##
## check for inconsistent data: since the rows in the original table
## correspond to board memberships, there frequently are repeated
## rows for the same person, so check that their information is
## consistent i.e. person attributes like Gender and Age have the
## same value for every row for the same person
##
print('verifying that person attributes are consistent...')
for (attrname in c("Gender", "Age")) {
  for (person in unique(dat$PersonID)) {
    attrs <- dat[which(dat$PersonID == person), attrname]
    stopifnot(length(unique(attrs)) == 1)
  }
}

## 
## get binary attributes
##
## female is for people only no companies
## company just is 1 for company or 0 for person

binattr <- data.frame(company = ifelse(V(g)$type == FALSE, 0, 1),
                      female  = ifelse(V(g)$type == FALSE,
                                ifelse(V(g)$Gender == 'M', 0,
                                    ifelse(V(g)$Gender == 'F', 1, NA)), NA))
#TODO edge not node attribute:    indep   = ifelse(V(g)$Indep. == "Y", 1, 0),
#TODO edge not node attribute:    nom     = ifelse(V(g)$Nom. == "Y", 1, 0),
#TODO edge not node attribute:    interim = ifelse(V(g)$Interim == "Y", 1, 0))
                      
summary(binattr)


##
## get categorical attributes
## These are all on people only not companies
##
catattr <- data.frame(gender  = ifelse(V(g)$type == FALSE,
                                 ifelse(V(g)$Gender == "NA", NA, V(g)$Gender),
                                 NA),
                      country = ifelse(V(g)$type == FALSE,
                                 ifelse(V(g)$Country == "NA", NA, V(g)$Country),
                                 NA))
#TODO edge not node attribute:  position= ifelse(V(g)$Position == "NA", NA, V(g)$Position))
## print the factor levels to stdout for future reference (codebook)
print("gender")
catattr$gender <- factor(catattr$gender)
print(levels(catattr$gender))
print("country")
catattr$country <- factor(catattr$country)
print(levels(catattr$country))
#print("position")
#catattr$position <- factor(catattr$position)
#print(levels(catattr$position))


##
## make binary ("one-hot") version of Gender, Position and Country attributes,
## and add to binary attributes
##

print('Recoding categorical as binary with one-hot encoding...')

catattr_recoded <- catattr
catattr_recoded$ID <- seq(1:nrow(catattr_recoded))
catattr_recoded <- dcast(data = melt(catattr_recoded, id.vars = "ID"),
                         ID ~ variable + value, fun.aggregate = length)
catattr_recoded$ID <- NULL
binattr <- cbind(binattr, catattr_recoded)

print('Fixing NA after one-hot encoding...')

# One-hot encoding above with melt and dcast adds an _NA dummy variable,
## and has 0 for for values that were NA. Use the _NA dummy to recode
## all dummy variables that were for an NA value back to NA

for (colname in c("gender", "country")) {
  NA_idx <- which(binattr[, paste(colname, "NA", sep="_")] == 1)
  dummyvarnames <- Filter(function(s) substr(s, 1, nchar(colname)+1) == paste(colname, '_', sep='') && s != paste(colname, "NA", sep="_"), names(binattr))
  for (varname in dummyvarnames) {
    binattr[NA_idx, varname] <- NA
  }
}


print('replacing _ with . in column names after melt/dcat...')

## Have to replace '_' with '.' in column names as reshape2 melt/dcast above
## introduces '_' 
colnames(binattr) <- sapply(colnames(binattr), function(s) gsub("_", ".", s))

# compare auto encoding to original gender binary coding to check
stopifnot(all(binattr$female == binattr$gender.F, na.rm = TRUE))


##
## convert categorical attributes to integer values (as written to stdout above)
##
summary(catattr)
catattr$gender <- as.numeric(catattr$gender)
catattr$country <- as.numeric(catattr$country)
#catattr$position <- as.numeric(catattr$position)
summary(catattr)
                       

##
## get continuous attributes
##
## Age is only people only not companies
##

## Appointed is days since January 1, 1970 (standard internal R format)
## This is OK as earliest appointed date is 1972-01-20
contattr <- data.frame(
         age = as.numeric(ifelse(V(g)$type == 0, 
                            ifelse(V(g)$Age == 0, NA, V(g)$Age), NA))
#TODO edge not node attribute:  appointed = as.numeric((as.Date(V(g)$Appointed, format = "%d/%m/%Y")))
  )
                     

## FIXME: fix the ages like 1971 which clearly are birth year, either
## convert to actual age by subtracting from 2022 or set to NA

##
## compute BiRank centrality and add as continuous attribute
##

elist <- as.data.frame(get.edgelist(g))
names(elist) <- c("person", "company")
cat("Computing birank centrality...\n")
system.time( bprank <- bipartite_rank(data = elist,
                                      normalizer = "BiRank",
                                      return_mode= "both"))
contattr$birank <- c(bprank$rows$rank, bprank$columns$rank)

##
## compute betweeneess centrality and add as continuous attribute
##

cat("Computing betweeneess centrality...\n")
system.time( contattr$betweenness <- betweenness(g, directed = FALSE, 
                                                    normalized = FALSE) )

summary(contattr)

##
## get outcome binary attribute
##
outcome <- data.frame(female = binattr$female)


###
### write graph
###


outfilename <- 'connect4_directors_bipartite.net'
if (get_giantcomponent) {
  outfilename <- 'connect4_directors_bipartite_gc.net'
}
## Writing graph in pajek format uses (as of when this 
## script was written, with igraph version 1.3.4) the internal
## integer node identifiers from 1..N which is just as 
## required for ALAAMEE or EstimNetDirected Pajek network format.
write.graph(g, outfilename, format="pajek")


##
## write binary attributes
##

write.table(binattr,
            file = ifelse(get_giantcomponent,
                          "connect4_directors_binattr_gc.txt", 
                          "connect4_directors_binattr.txt"),
            row.names = FALSE, col.names = TRUE, quote = FALSE)

##
## write categorical attributes
##

write.table(catattr,
            file = ifelse(get_giantcomponent,
                          "connect4_directors_catattr_gc.txt", 
                          "connect4_directors_catattr.txt"),
            row.names = FALSE, col.names = TRUE, quote=FALSE)

##
## write continuous attributes
##

write.table(contattr,
            file = ifelse(get_giantcomponent,
                          "connect4_directors_contattr_gc.txt", 
                          "connect4_directors_contattr.txt"),
            row.names = FALSE, col.names = TRUE, quote = FALSE)

##
## write outcome binary attribute
##

write.table(outcome,
            file = ifelse(get_giantcomponent,
                          "connect4_directors_outcome_gc.txt", 
                          "connect4_directors_outcome.txt"),
            row.names = FALSE, col.names = TRUE, quote = FALSE)

##
## Write nodeid file that maps integer node id (1..N) to original
## identifier, so that we can cross-reference back to original data
## if necessary
##
nodeid <- data.frame(nodeID = 1:vcount(g), origID = V(g)$name)
write.table(nodeid,
            file = ifelse(get_giantcomponent,
                          "connect4_directors_nodeid_gc.txt", 
                          "connect4_directors_nodeid.txt"),
            row.names = FALSE, col.names = TRUE, quote = FALSE)

## end
