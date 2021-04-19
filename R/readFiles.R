#
# File:    readFiles.R
# Author:  Alex Stivala
# Created: September 2015
#
# 
# Functions for reading and writing graph matrix files, attributes, etc.
#

library(igraph)

#
# read_graph_file() - read adjacency matrix in paralle spnet (matrix) format
#                     or Pajek format
# 
# Parameters:
#     filename - filename of graph file to read from
#     directed - TRUE for directed graph
#
# Return value:
#     igraph graph object built from data in file
#
read_graph_file <- function(filename, directed) {
  alltext <- readLines(filename)
  if (any(grepl('*matrix', alltext, fixed=TRUE))) {
      return (read_graph_matrix_file(filename, directed))
  } else {
      pajek_text <- alltext
      if (any(grepl('***This graph contains:****', alltext, fixed=TRUE))) {
          # remove extra lines written by PNet
          pajek_text <- alltext[1:which(alltext == '***This graph contains:****')-1]
      }
      # remove all the vertex lines that don't seem to work with igraph pajek format
      firstline <- pajek_text[1]
      pajek_text <- pajek_text[(which(grepl('^[*]', pajek_text[2:length(pajek_text)]))+1):length(pajek_text)]
      tmpfilename <- tempfile()
      write(firstline, file=tmpfilename)
      write(pajek_text, file=tmpfilename, append=TRUE)
      g <- read.graph(tmpfilename, format="pajek")
      unlink(tmpfilename)
      stopifnot(is.directed(g) == directed)
      return(g)
  }
}

#
# read_graph_matrix_file() - read adjacency matrix in paralle spnet format
# 
# Parameters:
#     filename - filename of subgraph file to read from
#     directed - TRUE for directed graph
#
# Return value:
#     igraph graph object built from adjacency matrix
#
read_graph_matrix_file <- function(filename, directed) {
  # skip all lines that do not start with 0 or 1
  # this includes the first two lines *vertices n and *matrix as well as
  # all lines following the actual matrix with various stats etc.
  # which SPnet writes there (but not snowballSample.R)
  alltext <- readLines(filename)
  matrixtext <- grep("^[01][01 ]+$", alltext, value=T)
  adjmatrix <- as.matrix(read.table(textConnection(matrixtext)))
  if (directed) {
      g <- graph.adjacency(adjmatrix, mode='directed')
  } else {
      g <- graph.adjacency(adjmatrix, mode='undirected')
  }
  return(g)
}

#
# read_attr_file() - read attributes file in one-column format  
#                      NB node nubmers are assumed to be ordered 1,2,3...N
#
# Parameters:
#      filename - filename to read from
#
# Return value:
#      vector of attribute values
#
read_attr_file <- function(filename) {
    attr_df <- read.table(filename, header=F, skip=1)
    return(attr_df$V1)
}

#
# read_attr_file_multi() - read multiple attributes file in multi-column format 
#                      NB node nubmers are assumed to be ordered 1,2,3...N
#
# Parameters:
#      filename - filename to read from
#
# Return value:
#      data frame of attribute values
#
read_attr_file_multi <- function(filename) {
    attr_df <- read.table(filename, header=T)
    return(attr_df)
}

#
# read_outcome_file() - read attributes file in one-column format  
#                      with single-line header (Pajek) ignored as first line
#                      NB node nubmers are assumed to be ordered 1,2,3...N
#
# Parameters:
#      filename - filename to read from
#
# Return value:
#      vector of attribute values
#
read_outcome_file <- function(filename) {
    attr_df <- read.table(filename, header=F, skip=1)
    return(attr_df$V1)
}

# write_outcome_file() - write attr file with header
#
# Parameters:
#    filename - filename to write to (warning: overwritten)
#    attrs  - vector of attr values
#             elemetn i of the vector corresponds to node i of graph (1..N)
#
# Return value:
#    None.
#
write_outcome_file <- function(filename, attrs) {
  f <- file(filename, open="wt")
  cat('outcome\n', file=f)
  write.table(attrs, file=f, append=T, row.names=F, col.names=F)
  close(f)
}


#
#
# write_attr_file() - write outcome file in parallel spnet (Pajek .clu) file format
#
# Parameters:
#    filename - filename to write to (warning: overwritten)
#    outcomes  - vector of outcome values
#             elemetn i of the vector corresponds to node i of graph (1..N)
#    name     - name of attribute for header line
#
# Return value:
#    None.
#
write_attr_file <- function(filename, outcomes, name) {
  f <- file(filename, open="wt")
  cat(name, '\n', file=f)
  write.table(outcomes, file=f, append=T, row.names=F, col.names=F)
  close(f)
}

#
#
# write_attr_file_multi() - write attributes file in multicolumn format
#
# Parameters:
#    filename - filename to write to (warning: overwritten)
#    attrs  - data frame of attribute values
#             row i of the data frame corresponds to node i of graph (1..N)
#
# Return value:
#    None.
#
write_attr_file_multi <- function(filename, attrs) {
  f <- file(filename, open="wt")
  write.table(attrs, file=f, row.names=F, col.names=T)
  close(f)
}


#
# write_zone_file() - write zone file with header
#
# Parameters:
#    filename - filename to write to (warning: overwritten)
#    zones  - vector of snowball zones (waves) 0..n (0 for seed node)
#             elemetn i of the vector corresponds to node i of graph (1..N)
#
# Return value:
#    None.
#
write_zone_file <- function(filename, zones) {
  f <- file(filename, open="wt")
  cat('zone\n', file=f)
  write.table(zones, file=f, row.names=F, col.names=F)
  close(f)
}

