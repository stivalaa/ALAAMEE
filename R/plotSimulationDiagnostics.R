#!/usr/bin/Rscript
##
## File:    plotSimulationDiagnostics.R
## Author:  Alex Stivala
## Created: November 2019
##
## Derived from plotPNetSimulationDiagnostics.R  (ADS Feb. 2014);
## also plotPNetGofDiagnostics.R (ADS Feb. 2014)
##
## Similarly to the SPSS script genreated by PNet simulation or GoF, plot
## scatterplot to show autocorrelation in samples and histograms of network
## statisics, for use on UNIX version instead of the SPSS script.
##
## Loess smoothed line on scatterplot and mean on histogram are plotted
## in blue dashed lines. On histogram 95% CI is ploted as dotted blue lines.
##
##
## Usage: Rscript plotSimulationDiagnostics.R simulation_stats_output.txt
##                                            [obs_stats.txt]
##
## e.g.: Rscript ../scripts/plotSimulationDiagnostics.R stats_sim_n1000_binattr_sample.txt  obs_stats_n1000_sample_0.txt
##
## If the optional observed stats filename is specified, then the
## observed stats of a single network are read from this and plotted
## in red on the plots for comparison to the simulated stats.
## These observed stats are from the output of e.g.
## compuateALAAMstatisticsSimpleDemo.py, which is just two white-space
## deliited lines with names of stats as first (header) line and the
## values as the second line, e.g.:
##
## Density Activity Contagion Binary Continuous
## 80.0 526.0 95.0 58.0 47.54103699999999
##
##
## The t-ratios of the statistics are also computed and written to stdout,
## as is Mahalanobis distance of the observed stats vector from the
## distribution of the simulated stats vectors.
##
## Output is postscrpt file basename.eps where basename is from the input
## file e.g. stats_sim_n1000_binattr_sample-plots.eps
##
##
library(grid)
library(gridExtra)
library(ggplot2)
library(reshape)
library(scales)
library(MASS) #for ginv()

zSigma <- 1.96 # number of standard deviations for 95% confidence interval

# http://stackoverflow.com/questions/10762287/how-can-i-format-axis-labels-with-exponents-with-ggplot2-and-scales
orig_scientific_10 <- function(x) {
  parse(text=gsub("e", " %*% 10^", scientific_format()(x)))
}
my_scientific_10 <- function(x) {
# also remove + and leading 0 in exponennt
  parse( text=gsub("e", " %*% 10^", gsub("e[+]0", "e", scientific_format()(x))) )
}

args <- commandArgs(trailingOnly=TRUE)
if (length(args) < 1 || length(args) > 2) {
    cat("Usage: Rscript plotSimulationDiagnostics.R simulation_stats.txt [obs_stats.txt]\n")
    quit(save='no')
}
simstats_filename <- args[1]
basefilename <- sub("(.+)[.].+", "\\1", basename(simstats_filename))
do_obs <- FALSE
if (length(args) == 2) {
  obs_stats_filename <- args[2]
  do_obs <- TRUE
}


simstats <- read.table(simstats_filename, header=TRUE, stringsAsFactors=FALSE)
simstats0 <- data.frame(simstats)

statnames <- names(simstats)[names(simstats) != "t"]

if (do_obs) {
  obsstats <- read.table(obs_stats_filename, header=TRUE, stringsAsFactors=FALSE)
  stopifnot(nrow(obsstats) == 1)
}

simstats <- melt(simstats, id=c('t'))
plotlist <- list()
if (do_obs) {
  cat('effect','observed', 'mean', 'sd', 't_ratio', '\n')
}
for (statname in statnames) {
    simstats_statname <- simstats[which(simstats$variable == statname),]

    p <- ggplot(simstats_statname, aes(x=t, y=value))
    p <- p + geom_point()
    p <- p + geom_smooth(method = loess, color = "blue", linetype = "dashed",
                         se = FALSE)
    if (do_obs && !(statname %in% c("AcceptanceRate", "acceptance_rate"))) {
      p <- p + geom_hline(yintercept = obsstats[1,statname],
                          color = "red")
    }
    p <- p + xlab('t')
    p <- p + ylab(statname)
    p <- p + scale_x_continuous(guide = guide_axis(check.overlap = TRUE,
                                                   #n.dodge = 2,
                                                   #angle = 90
                                                  ),
                                labels = my_scientific_10)
    plotlist <- c(plotlist, list(p))

    p <- ggplot(simstats_statname, aes(x=value))
    p <- p + geom_histogram()
    p <- p + geom_vline(aes(xintercept = mean(value)), color = "blue",
                        linetype = "dashed")
    p <- p + geom_vline(aes(xintercept = mean(value) -
                            zSigma*sd(value)), 
                        colour='blue', linetype='dotted')
    p <- p + geom_vline(aes(xintercept = mean(value) +
                            zSigma*sd(value)), 
                        colour='blue', linetype='dotted')
    if (do_obs &&  !(statname %in% c("AcceptanceRate", "acceptance_rate"))) {
      p <- p + geom_vline(xintercept = obsstats[1,statname],
                          color = "red")
    }
    p <- p + xlab(statname)
    p <- p + scale_x_continuous(guide = guide_axis(check.overlap = TRUE,
                                                   #n.dodge = 2,
                                                   #angle = 90
                                                  ))
    plotlist <- c(plotlist, list(p))

    ## compute t-ratio
    if (do_obs && !(statname %in% c("AcceptanceRate", "acceptance_rate"))) {
      simstatvalues<- simstats[which(simstats$variable == statname),"value"]
      t_ratio <- (mean(simstatvalues) - obsstats[1,statname])/sd(simstatvalues)
      cat(statname, obsstats[1,statname], mean(simstatvalues),
           sd(simstatvalues), t_ratio, '\n')
    }
}

postscript(paste(basefilename, '-plots.eps', sep=''), onefile=FALSE,
           horizontal = TRUE)
##           paper="special", horizontal=FALSE, width=9, height=6)
do.call(grid.arrange, plotlist)
dev.off()

##
## Mahalanobis distance
##

if (do_obs) {  # only possible if we have observed stats vector
  ## First get stats in both observed and simulatd, and reorder so
  ## they match
  
  Z <- simstats0[ , names(simstats0)[!(names(simstats0) %in% c('t', 'AcceptanceRate', 'acceptance_rate', 'meanDegree1', 'varDegree1', 'meanDegree0', 'varDegree0'))]]
  statnames <- intersect(names(Z), names(obsstats))
  Z <- Z[ , names(Z)[names(Z) %in% statnames]]
  obsstats <- obsstats[, names(obsstats)[names(obsstats) %in% statnames]]
  nameorder <- order(statnames)
  Z <- Z[ , nameorder]
  obsstats <- obsstats[ , nameorder]
  obsstats <- as.matrix(obsstats) # convert from dataframe to 1d matrix
  
  cat("Using statistics: ", statnames[nameorder], "\n")
  
  ## Recompute t-ratios just as a check
  cat('t-ratios:\n')
  print( (colMeans(Z) - obsstats) / apply(Z, 2, sd) )
  
  ## Get covariance matrix and invert, checking for ill-conditioned
  ## (computationally singular) covariance matrix first, and if so,
  ## use instead Moore-Penrose pseudoinverse.
  Sigma <- cov(Z)
  if (rcond(Sigma) < .Machine$double.eps) {
    warnmsg <- "WARNING: covariance matrix is computationally singular, using pseudo-inverse of covariance matrix\n"
    cat(warnmsg, file=stderr())
    cat(warnmsg)
    SigmaInverse <- ginv(Sigma) # generalized (Moore-Penrose) inverse
  } else {
    SigmaInverse <- solve(Sigma) # matrix inverse
  }
  #print(Sigma)#XXX
  #print(SigmaInverse)#XXX
  
  ## mahalanobis() returns squared Mahalanobis distance
  mdist1 <- sqrt(mahalanobis(obsstats, colMeans(Z), SigmaInverse, inverted=TRUE))
  #print(dim(obsstats - colMeans(Z)))#XXX
  #print(dim(SigmaInverse))#XXX
  mdist2 <- sqrt((obsstats - colMeans(Z)) %*% SigmaInverse %*% t(obsstats - colMeans(Z))) #XXX check same as mahalanobis()
  print(mdist1)#XXX
  print(mdist2)#XXX
  cat('Mahalanobis distance: ', mdist1, '\n')
}
