##!/usr/bin/Rscript
##
## File:    convertSNAPgithubToALAAMEEFormat.R
## Author:  Alex Stivala
## Created: May 2023
##
## Read the network and attributes data for the Github  social
## network from SNAP http://snap.stanford.edu/data/git_web_ml.zip
## and convert to Pajek format for ALAAMEE or EstimNetDirected.  See
## documentation in
## http://snap.stanford.edu/data/github-social.html
## and source citation:
##
## Rozemberczki, B., Allen, C., & Sarkar, R. (2021). Multi-scale
## attributed node embedding. Journal of Complex Networks, 9(2),
## cnab014.
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
## See also: https://github.com/benedekrozemberczki/MUSAE
##
##
## Usage:
## 
## Rscript convertSNAPgithubToALAAMEEFormat.R git_web_ml.zip
##
## git_web_ml.zip is the zip file downloaded from
## http://snap.stanford.edu/data/git_web_ml.zip
##
## Output files in cwd (WARNING overwritten):
##   musae_git.net
##   musae_git_target.txt
##e

library(igraph)

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 1) {
  cat("Usage: convertSNAPgithubToALAAMEEFormat.R git_web_ml.zip\n")
  quit(save="no")
}
zipfile <- args[1]

## Dataset information
##
## A large social network of GitHub developers which was collected
## from the public API in June 2019. Nodes are developers who have
## starred at least 10 repositories and edges are mutual follower
## relationships between them. The vertex features are extracted based
## on the location, repositories starred, employer and e-mail
## address. The task related to the graph is binary node
## classification - one has to predict whether the GitHub user is a
## web or a machine learning developer. This target feature was
## derived from the job title of each user.

## zipfile contents:
##
## unzip -t ~/SwitchDrive/Institution/USI/datasets/SNAP_Datasets/musae-github/git_web_ml.zip 
## Archive:  /home/alex/SwitchDrive/Institution/USI/datasets/SNAP_Datasets/musae-github/git_web_ml.zip
##     testing: git_web_ml/              OK
##     testing: git_web_ml/musae_git_edges.csv   OK
##     testing: git_web_ml/musae_git_features.json   OK
##     testing: git_web_ml/musae_git_target.csv   OK
##     testing: git_web_ml/citing.txt    OK
##     testing: git_web_ml/README.txt    OK
## No errors detected in compressed data of /home/alex/SwitchDrive/Institution/USI/datasets/SNAP_Datasets/musae-github/git_web_ml.zip.

## From http://snap.stanford.edu/data/github-social.html
##
## Dataset statistics
## Directed	No.
## Node features	Yes.
## Edge features	No.
## Node labels	Yes. Binary-labeled.
## Temporal	No.
## Nodes	37,700
## Edges	289,003
## Density	0.001
## Transitvity	0.013

outfilename_undirected <- "musae_git.net"
targetfilename <- "musae_git_target.txt"

##
## network
##
edgelist <- read.table(unz(zipfile,
                           'git_web_ml/musae_git_edges.csv'),
                       header = TRUE,  stringsAsFactors = FALSE, sep = ',')

uniqueIds <- unique(c(edgelist$id_1, edgelist$id_2))
numIds <- length(uniqueIds)
cat('number of unique ids is ', numIds, '\n')
cat('min is ', min(uniqueIds), ' max is ', max(uniqueIds), '\n')


## The Github data has nodes numbered 0..N-1 (N = 37700)
stopifnot(min(uniqueIds) == 0)
stopifnot(max(uniqueIds) == numIds - 1)
stopifnot(numIds == 37700)

## have to add 1 as igraph cannot handle 0 as vertex id apparently
g <- graph.edgelist(as.matrix(edgelist)+1, directed=FALSE)


summary(g)
## remove multiple and self edges
g <- simplify(g , remove.multiple = TRUE, remove.loops = TRUE)
summary(g)

## Nodes	37,700
## Edges	289,003

stopifnot(vcount(g) == 37700)
stopifnot(ecount(g) == 289003)


##
## read binary target attribute This target feature was
## derived from job title, and indicates whether the uer is a web or
## machine learning developer.
##

target <- read.table(unz(zipfile,
                         'git_web_ml/musae_git_target.csv'),
                     header = TRUE, stringsAsFactors = FALSE, sep = ',')
## Make sure it really does line up with the node ids 0..N-1
stopifnot(nrow(target) == numIds)
stopifnot(min(target$id) == 0)
stopifnot(max(target$id) == numIds - 1)
stopifnot(all(target$id == seq(0, vcount(g)-1)))

##
## get binary attributes
##

## TODO there seems to be no documentation of how this is coded,
## neither in the README or in the paper: is 1 for web or ml developer?

outcomebinattr <- data.frame(devtype = target[, "ml_target"]) 
summary(outcomebinattr)


## TODO read and process musae_git_features.json This JSON format
## file gives a list of features (integers) based on location, starred
## repositories, employer, and email addresses of
## users. So this could then be used as attribute for categorical set
## similarity (Jaccard) in EstimNetDirected.


##
## Write network
##
write.graph(g, outfilename_undirected, format="pajek")


##
## write outcome binary attribute
##

write.table(outcomebinattr, file = targetfilename, row.names = FALSE,
            col.names = TRUE, quote = FALSE)
