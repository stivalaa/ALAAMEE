##!/usr/bin/Rscript
##
## File:    convertConnect4BoardDirectorAffiliationsToALAAMEEFormatCentrality.R
## Author:  Alex Stivala
## Created: September 2022
##
## Read the network and attributes data in CSV format for the 
## Connect4 Boardrooom company director network 
## and convert to Pajek bipartite format for ALAAMEE or EstimNetDirected.
## Also compute betweenness centrality and BiRank centrality measures
## for all the nodes.
##
## Usage: Rscript convertConnect4BoardDirectorAffiliationsToALAAMEEFormatCentrality.R [-g] search.csv ASXListedCompanies.csv ASXForeignEntityReport.xlsx
##
## where 
##
## search.csv is the query result from selecting all companies and
## all directors from the Connect 4 Boardroom database.
## Accessed from Swinburne at https://www-connect4-com-au.eu1.proxy.openathens.net/cms/boardroom/index.html
## (14 September 2022 by Peng at Swinburne).
##
## and 
##
## ASXListedCompanies.csv is the list of ASX listed companies 
## (with name, code, GICS industry group, market capitalization)
## downloaded from the Australian Stock Exchange (ASX) 
##   https://www2.asx.com.au/markets/trade-our-cash-market/directory
##
## and
##
##  ASX-foreign-entity-report.xlsx
##  shows "selected securities" of foreign incorporated entities quoted on
##  the ASX 
##  downloaded from https://www2.asx.com.au/content/dam/asx/documents/listings/foreign-entity-data/2022/ASX-foreign-entity-report-20220930.xlsx
##  See:
##   https://www2.asx.com.au/listings/how-to-list/listing-requirements/foreign-entity-data
##
## The Connect 4 Boardroom database ia a Thomson Reuters commercial
## prodct:
## https://legal.thomsonreuters.com.au/products/connect4/boardroom.aspx
## For ASX data see
## https://www2.asx.com.au/legals/data-disclaimers 
## for terms and conditions (Thomson Reuters, MorningStar)
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
##     connect4_directors_catattr_strings.txt
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
##
library(readxl) # For reading ASX foreign entity report .xlsx file
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
if (length(args) < 3 || length(args) > 4 ||
    (length(args) == 4 && args[1] != "-g")) {
  cat("Usage: convertConnect4BoardDirectorAffiliationsToALAAMEEFormatCentrality.R [-g] search.csv ASXListedCompanies.csv ASXForeignEntityReport.xlsx\n")
  quit(save="no")
} else if (length(args) == 4) {
  get_giantcomponent <- TRUE
  infile <- args[2]
  asxfile <- args[3]
  asxforeign_file <- args[4]
} else {
  infile <- args[1]
  asxfile <- args[2]
  asxforeign_file <- args[3]
}

##
## Read Connect 4 Boardroom data
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

## remove any records for the ASX test security TES
print(nrow(dat))
print("removing rows for ASX test security TES")
dat <- dat[which(dat$Code != "TES"), ]
print(nrow(dat))

##
## Read ASX listed companies data
##

## the data looks like this:
#"ASX code","Company name","Listing date","GICs industry group","Market Cap"
#"14D","1414 DEGREES LIMITED","2018-09-12","Capital Goods",14542953
#
## Note market cap is in AUD, e.g. the first row
## "14D","1414 DEGREES LIMITED","2018-09-12","Capital Goods",14542953
## shows on the rendering at https://www2.asx.com.au/markets/trade-our-cash-market/directory
## as $14.54M
## Note also in the header line "GICs" [sic] not "GICS" indsutry group.
# 
cat("reading ", asxfile, "...\n")
system.time(asx <- read.csv(asxfile, header = TRUE, stringsAsFactors = FALSE) )
i = match("GICs.industry.group", names(asx))
if (!is.na(i)) {
  names(asx)[i] <- "GICS.industry.group" # fix the header typo GICs for GICS
}

##
## Read ASX foreign entity report Excel .xlsx file
##

## the data being an Excel spreadsheet if formatted (with headers, logos,
## footnotes, formatting etc.) for human readability not for machine reading
## reproducibility, etc. But the readxl package handles it.
## The header looks like this:
##      ASX Code        Entity Name     Country of Incorporation        Security Description    ASX Listing or ASX Foreign Exempt Listing       Securities quoted on ASX as at end of September 20221 (Millions)        Securities held in Australia as at end of September 20221 (Millions)            
##
## read_excel() seems to automatically handle getting rid all of the logos, text
## etc. before the actual table header, but the footnotes etc. after the table
## are still there, but with NA in every field except ASX Code. So we will
## just get rid of those ones. WARNING: this depens on the particular format
## of this instance of the Excel file
## downloaded from https://www2.asx.com.au/content/dam/asx/documents/listings/foreign-entity-data/2022/ASX-foreign-entity-report-20220930.xlsx
## (downloaded 23 Oct 2022) - relying on Excel format and readxl package
## is inherently unreliable, but that's just unavoidable when data is
## distributed as Excel files instead of CSV or other more sensible formats.
##
asxforeign <- read_excel(asxforeign_file)
asxforeign <- asxforeign[which(!is.na(asxforeign$'Entity Name')),]
## ASX listing data uses "United States" but this uses 
## "United States of America" so makenew column with soncistent name
asxforeign$Country <- gsub("United States Of America", "United States", asxforeign$`Country of Incorporation`)

## Note we will build a column Country which is country of residence for
## director and country of incorporation for company (rather than NA for
## one mode for most attributes) - so can use in ERGM for example as 
## catetgorical matching on this attribute between the two diferent modes
## (node types). Similarly for binary attribute notAustralia.

## 
## Merge the Connect 4 Boardroom data and ASX list
##
dat <- merge(x = dat, y = asx, by.x = "Code", by.y = "ASX.code", all.x = TRUE)

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

person_attrs <- c('Gender', 'Country', 'Age', "Surname","First Name","Middle Name","Known As","P.ID")
company_attrs <- c('GICS.industry.group', "Code", "Company", "Company.name", "Listing.date", "Market.Cap")
all_attrs <- c('company', person_attrs, company_attrs)

##
## check for inconsistent data: since the rows in the original table
## correspond to board memberships, there frequently are repeated
## rows for the same person, so check that their information is
## consistent i.e. person attributes like Gender and Age have the
## same value for every row for the same person
##
print('verifying that person attributes are consistent...')
for (attrname in person_attrs) {
  for (person in unique(dat$PersonID)) {
    attrs <- dat[which(dat$PersonID == person), attrname]
    stopifnot(length(attrs) == 0 || length(unique(attrs)) == 1)
  }
}
print('verifying that company attributes are consistent...')
for (attrname in company_attrs) {
  for (company in unique(dat$CompanyID)) {
    attrs <- dat[which(dat$CompanyID == company), attrname]
    stopifnot(length(attrs) == 0 || length(unique(attrs)) == 1)
  }
}




##
## Build director affiliation network
##

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
# first set all to NA
for (colname in all_attrs) {
  g <- set.vertex.attribute(g, colname, value = NA)
}
# person attributes
print("person attributes")
for (colname in person_attrs) {
  print(colname)
  for (personid in unique(dat$PersonID)) {
    # note the [1] after which() here, to get the first matching row for
    # that personid: it may match several rows, but we checked above that
    # these all have the same attribute values, so getting the first is safe.
    val <- dat[which(dat$PersonID == personid)[1], colname]
    g <- set.vertex.attribute(g, colname, V(g)[personid], 
                              ifelse(length(val) == 0, NA, val))
  }
}
# company attributes
print("company attributes")
for (colname in company_attrs) {
  print(colname)
  for (companyid in unique(dat$CompanyID)) {
    # note the [1] after which() here, to get the first matching row for
    # that companyid: it may match several rows, but we checked above that
    # these all have the same attribute values, so getting the first is safe.
    g <- set.vertex.attribute(g, colname, V(g)[companyid],
                             dat[which(dat$CompanyID == companyid)[1], colname])
  }
}

## special handling for Country for companies: set to Australia except
## for comapnies that are in the ASX foreign entity report
print("Country attribute for companies")
for (companyid in unique(dat$CompanyID)) {
  asxcode <- dat[which(dat$CompanyID == companyid),"Code"][1]
  if (asxcode %in% asxforeign$`ASX Code`) {
    ###cat('XXX1 asxcode = ', asxcode,'\n')
    ###cat('XXX2 ')
    ###print(asxforeign[which(asxforeign$`ASX Code` == asxcode),])#XXX
    g <- set.vertex.attribute(g, "Country", V(g)[companyid],
            asxforeign[which(asxforeign$`ASX Code` == asxcode),]$Country)
  } else {
    g <- set.vertex.attribute(g, "Country", V(g)[companyid], "Australia")
  }
}


summary(g)

# there can be no self edges (since it is bipartite)
stopifnot(!any_loop(g))

## remove multiple edges (these can occur in this data as each row in the
## table is an appointment, so can be appointed to same board in difference
## capacities for example)
print('removing multiple edges...')
g <- simplify(g , remove.multiple = TRUE, remove.loops = FALSE)
summary(g)


# Public companies must have at least three directors
# see e.g. https://asic.gov.au/for-business/registering-a-company/steps-to-register-a-company/minimum-officeholders/
stopifnot(min(degree(g, which(V(g)$type == TRUE))) >= 3)


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
## Also replace '-' with '.' and '/' with '.' and ',' with '.'
## and also '(' and ')' with '.' (occurs in "Virgin Islands (British)")
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
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub(",", ".", s)))
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub("(", ".", s, fixed = TRUE)))
  g <- set.vertex.attribute(g, colname,
                            value = sapply(get.vertex.attribute(g, colname),
                                           function(s) gsub(")", ".", s, fixed = TRUE)))
}


## 
## get binary attributes
##
## female is for people only no companies
## company just is 1 for company or 0 for person
## Also add notAustralia for country not Australia, for both country and person
binattr <- data.frame(company = ifelse(V(g)$type == FALSE, 0, 1),
                      female  = ifelse(V(g)$type == FALSE,
                                ifelse(V(g)$Gender == 'M', 0,
                                    ifelse(V(g)$Gender == 'F', 1, NA)), NA),
                      notAustralia = ifelse(V(g)$Country == "Australia", 0, 1)
                     )
#TODO edge not node attribute:    indep   = ifelse(V(g)$Indep. == "Y", 1, 0),
#TODO edge not node attribute:    nom     = ifelse(V(g)$Nom. == "Y", 1, 0),
#TODO edge not node attribute:    interim = ifelse(V(g)$Interim == "Y", 1, 0))
                      
summary(binattr)


##
## get categorical attributes
## Person attributes only: gender
## Company attributes only: industryGroup  (GICS.industry.group)
## Both modes: country (residence for diretor, incorporation for company)
##
catattr <- data.frame(gender  = ifelse(V(g)$type == FALSE,
                                 ifelse(V(g)$Gender == "NA", NA, V(g)$Gender),
                                 NA),
                      country = ifelse(V(g)$Country == "NA", NA, V(g)$Country),
                      industryGroup = ifelse(V(g)$type == FALSE, NA,
                         ifelse(is.na(V(g)$GICS.industry.group)            |
                                  V(g)$GICS.industry.group == "Not.Applic" |
                                  V(g)$GICS.industry.group == "Class.Pend" |
                                  V(g)$GICS.industry.group == "",
                                  NA,
                                V(g)$GICS.industry.group))
                     )


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
print("industryGroup")
catattr$industryGroup <- factor(catattr$industryGroup)
print(levels(catattr$industryGroup))

# There are 24 GICS industry groups
# see https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard
stopifnot(length(levels(catattr$industryGroup)) == 24)


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

#for (colname in c("gender", "country")) {
for (colname in c("gender")) {
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
# also check country Australia for consistency
stopifnot(all(!binattr$country.Australia == binattr$notAustralia, na.rm = TRUE))

##
## convert categorical attributes to integer values (as written to stdout above)
##
summary(catattr)
## Also make copy of original categorical attributes data frame
## with strings before conversion to factors, for future referene and
## easier data summary table creation for readability (strings not coded)
catattr_strings <- catattr
catattr$gender <- as.numeric(catattr$gender)
catattr$country <- as.numeric(catattr$country)
#catattr$position <- as.numeric(catattr$position)
catattr$industryGroup <- as.numeric(catattr$industryGroup)
summary(catattr)
                       

##
## get continuous attributes
##
## Age is only people only not companies
## Listing.date and Market.Cap are only companies not people
## Listing.date is converted to numeric year of listing date
##   note Listing.date is in format %Y-%m-%d but '-' already converted to '.'
##   note oldest year is 1885 (BHP) but that is an outlier:
##    > summary( as.numeric(format(as.Date(asx$Listing.date, format = "%Y-%m-%d"), format = "%Y")) )
##      Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's
##      1885    2002    2009    2007    2017    2022      13

## Market.Cap is in AUD, also convert to millions of AUD and log AUD


contattr <- data.frame(
         age = as.numeric(ifelse(V(g)$type == 0, 
                            ifelse(V(g)$Age == 0, NA, V(g)$Age), NA)),
         ListingYear = ifelse(V(g)$type == 1,
                          as.numeric(format(as.Date(asx$Listing.date, 
                                         format = "%Y-%m-%d"), format = "%Y")),
                          NA),
         MarketCap = ifelse(V(g)$type == 1, as.numeric(V(g)$Market.Cap), NA)
  )
contattr$MarketCapM <- round(contattr$MarketCap / 1e06, digits = 2)
contattr$logMarketCap <- log(contattr$MarketCap)
# replace -Inf with NA (for zero values with log; actually only one of these)
contattr$logMarketCap <- ifelse(is.infinite(contattr$logMarketCap), NA,
                                contattr$logMarketCap)

## Appointed is days since January 1, 1970 (standard internal R format)
## This is OK as earliest appointed date is 1972-01-20
#TODO edge not node attribute:  appointed = as.numeric((as.Date(V(g)$Appointed, format = "%d/%m/%Y")))
                     

##
## fix the ages like 1971 which clearly are birth year, either
## convert to actual age by subtracting from current year
##
print('fixing ages that are acutally birth years...')
#acutally to be consistent we choul fix curr_year to 2022 which is the year
#the data were downloaded, since all the other ages are ages in 2022
#curr_year <- as.numeric(format(Sys.Date(), "%Y"))
curr_year <- 2022
bad_age_rows <- which(contattr$age >= 1900)
print(contattr[bad_age_rows, ])#XXX
contattr[bad_age_rows, "age"] <- curr_year - contattr[bad_age_rows, "age"]
print(contattr[bad_age_rows, ])#XXX

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

summary(contattr)


##
## scale and center the centrality measures so regression coefficients not
## huge (e.g. birank) or tiny (eg. betweenness)
##

contattr$birank.scaled        <- scale(contattr$birank, center = TRUE, scale = TRUE)
contattr$betweenness.scaled   <- scale(contattr$betweenness, center = TRUE, scale = TRUE)
contattr$harmonic.cent.scaled <- scale(contattr$harmonic.cent, center = TRUE, scale = TRUE)

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

write.table(catattr_strings,
            file = ifelse(get_giantcomponent,
                          "connect4_directors_catattr_strings_gc.txt", 
                          "connect4_directors_catattr_strings.txt"),
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
