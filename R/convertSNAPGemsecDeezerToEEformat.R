##!/usr/bin/Rscript
##
## File:    convertGNAPGemsecDeezerToALAAMEEFormat.R
## Author:  Alex Stivala
## Created: March 2024
##
## Read the network and attributes data for the GEMSEC Deezer social
## network from SNAP http://snap.stanford.edu/data/gemsec_deezer_dataset.tar.gz
## and convert to Pajek format for ALAAMEE or EstimNetDirected.  See
## documentation in http://snap.stanford.edu/data/gemsec-Deezer.html
## and source citation:
##
## Rozemberczki, B., Davies, R., Sarkar, R., & Sutton, C. (2019,
## August). GEMSEC: Graph embedding with self clustering. In
## Proceedings of the 2019 IEEE/ACM international conference on
## advances in social networks analysis and mining (pp. 65-72).
##
## Reference for SNAP collection of data sets:
## 
##@misc{snapnets,
##  author       = {Jure Leskovec and Andrej Krevl},
##  title        = {{SNAP Datasets}: {Stanford} Large Network Dataset Collection},
##  howpublished = {\url{http://snap.stanford.edu/data}},
##  month        = jun,
##  year         = 2014
##}
##
##
## There are three separate networks and their corresponding JSON files
## with music genre data: Romania (RO), Croatia (HR), and Hungary (HU).
##
## Usage:
## 
## Rscript convertGNAPGemsecDeezerToALAAMEEFormat.R gemsec_deezer_dataset.tar.gz
##
## gemsec_deezer_dataset.tar.gz is the data set downloaded from
## http://snap.stanford.edu/data/gemsec_deezer_dataset.tar.gz
##
## Output files in cwd (WARNING overwritten):
##   deezer_ro_friendship.net
##   deezer_ro_binattr.txt
##   deezer_ro_contattr.txt
##   deezer_ro_outcome.txt
##   deezer_ro_outcome_alternative.txt
##   deezer_hu_friendship.net
##   deezer_hu_binattr.txt
##   deezer_hu_contattr.txt
##   deezer_hu_outcome.txt
##   deezer_hu_outcome_alternative.txt
##   deezer_hr_friendship.net
##   deezer_hr_binattr.txt
##   deezer_hr_contattr.txt
##   deezer_hr_outcome.txt
##   deezer_hr_outcome_alternative.txt
##

library(igraph)
library(jsonlite)

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 1) {
  cat("Usage: convertGNAPGemsecDeezerToALAAMEEFormat.R gemsec_deezer_dataset.tar.gz\n")
  quit(save="no")
}
targzfile <- args[1]

## .tar.gz file contents:
## tar ztvf data/gemsec_deezer_dataset.tar.gz 
## drwxrwxr-x adrijan/adrijan   0 2018-02-28 07:53 deezer_clean_data/
## -rw-rw-r-- adrijan/adrijan 4892019 2018-02-13 22:14 deezer_clean_data/HR_genres.json
## -rw-rw-r-- adrijan/adrijan 4053774 2018-01-31 21:41 deezer_clean_data/HU_genres.json
## -rw-rw-r-- adrijan/adrijan 3615864 2018-01-31 21:42 deezer_clean_data/RO_genres.json
## -rw-rw-r-- adrijan/adrijan 5769739 2018-01-31 21:42 deezer_clean_data/HR_edges.csv
## -rw-rw-r-- adrijan/adrijan 1443116 2018-01-31 21:42 deezer_clean_data/RO_edges.csv
## -rw-rw-r-- adrijan/adrijan 2565945 2018-01-31 21:41 deezer_clean_data/HU_edges.csv
## -rw-rw-r-- adrijan/adrijan    1367 2018-02-28 07:53 deezer_clean_data/dataset_descriptions.txt


## From the dataset_descriptions.txt file in .tar.gz file:
##
## We collected data from the music streaming service Deezer (November
## 2017). These datasets represent friendhips networks of users from 3
## European countries. Nodes represent the users and edges are the
## mutual friendships. We reindexed the nodes in order to achieve a
## certain level of anonimity. The csv files contain the edges --
## nodes are indexed from 0. The json files contain the genre
## preferences of users -- each key is a user id, the genres loved are
## given as lists. Genre notations are consistent across users. In
## each dataset users could like 84 distinct genres. Liked genre lists
## were compiled based on the liked song lists. The countries included
## are Romania, Croatia and Hungary. For each dataset we listed the
## number of nodes an edges.
##
## Country #Nodes   #Edges
## --------------------------	
## RO	41,773	 125,826
## HR	54,573	 498,202
## HU	47,538	 222,887
## --------------------------
##

## See also https://github.com/benedekrozemberczki/GEMSEC
## for original copy of data and more documentation

for (country in c("RO", "HR", "HU")) {
  cat(country, "\n")
  outfilename_undirected <- paste("deezer", tolower(country), "friendship.net",
                                  sep = "_")
  outcome_filename <- paste("deezer", tolower(country), "outcome.txt",
                            sep = "_")
  outcome_alt_filename <- paste("deezer", tolower(country),
                                "outcome_alternative.txt", sep = "_")  
  binattr_filename <-  paste("deezer", tolower(country), "binattr.txt",
                             sep = "_")
  contattr_filename <- paste("deezer", tolower(country), "contattr.txt",
                             sep = "_")
    
  ##
  ## network
  ##

  ## https://stackoverflow.com/questions/62592365/reading-a-specific-file-from-a-tar-file-via-readrds
  ## Apparently there is also an "archive" package to handle .tar.gz files
  ## but install in R failed on both cygwin and Linux so using shell pipes
  ## like:
  ## https://stackoverflow.com/questions/62592365/reading-a-specific-file-from-a-tar-file-via-readrds

  con <- pipe(paste('tar zxf', shQuote(targzfile), '-O',
                    shQuote(paste("deezer_clean_data/", country, "_edges.csv",
                                  sep=""))), 'rt')
  edgelist <- read.csv(con, header=TRUE)
  close(con)
  uniqueIds <- unique(c(edgelist$node_1, edgelist$node_2))
  numIds <- length(uniqueIds)
  cat('number of unique ids is ', numIds, '\n')
  cat('min is ', min(uniqueIds), ' max is ', max(uniqueIds), '\n')

  ## have to add 1 as igraph cannot handle 0 as vertex id apparently
  g <- graph.edgelist(as.matrix(edgelist)+1, directed=FALSE)

  summary(g)
  ## remove multiple and self edges
  g <- simplify(g , remove.multiple = TRUE, remove.loops = TRUE)
  summary(g)
  cat("density: ", graph.density(g), "\n")
  cat("transitivity: ", transitivity(g), "\n")

  ##
  ## Write network
  ##
  cat(outfilename_undirected, "\n")
  write.graph(g, outfilename_undirected, format="pajek")


  ##
  ## read genre information in JSON format
  ##

  con <- pipe(paste('tar zxf', shQuote(targzfile), '-O',
                    shQuote(paste("deezer_clean_data/", country,
                                  "_genres.json", sep=""))), 'rb')
  genres <- fromJSON(con)
  close(con)
  
  ## Make sure it really does line up with the node ids 0..N-1  
  stopifnot(length(genres) == vcount(g))
  stopifnot(min(as.integer(names(genres))) == 0)
  stopifnot(max(as.integer(names(genres))) == numIds - 1)

  ##
  ## Write genre frequency table to stout
  ##
  cat(country, "genre frequency:\n")
  print(table(unlist(genres)))

  ##
  ## Build continuous attributes
  ##

  ## number of genres that the user likes
  contattr <- data.frame(num_genres = sapply(genres, length))
  print(summary(contattr))


  ##
  ## Build outcome binary attribute
  ##

  ## The outcome binary attribute is 1 for liking any genre that
  ## contains "jazz" or 0 otherwise
  ## Approx 5% in each have this one
  unique_genres <- unique(unlist(genres))
  cat(country, "jazz genres:\n")
  cat(unique_genres[ unlist(sapply(unique_genres,
                            function(s) grepl("jazz", s,ignore.case=TRUE)))],
      '\n', sep = '|' )

  anyJazz <- lapply(genres, function(s) any(grepl("jazz", s,
                                                  ignore.case=TRUE)))
  outcomebinattr <- data.frame(anyJazz = as.integer(anyJazz))
  print(summary(outcomebinattr))

  ## The alternative outcome attribute is 1 for liking the "Alternative"
  ## genre
  ## Approx 30% to 40% in each have this one
  outcome_alt_binattr <- data.frame(alternative = as.integer(
                                      lapply(genres,
                                             function(v)
                                               "Alternative" %in% v)))
  print(summary(outcome_alt_binattr))
  
  ##
  ## Write continuous attributes
  ##
  cat(contattr_filename, "\n")
  write.table(contattr, file = contattr_filename, row.names = FALSE,
              col.names = TRUE, quote = FALSE)
  
  ##
  ## write outcome binary attribute
  ##
  cat(outcome_filename, "\n")
  write.table(outcomebinattr, file = outcome_filename, row.names = FALSE,
              col.names = TRUE, quote = FALSE)

  cat(outcome_alt_filename, "\n")
  write.table(outcome_alt_binattr, file = outcome_alt_filename,
              row.names = FALSE, col.names = TRUE, quote = FALSE)

}
