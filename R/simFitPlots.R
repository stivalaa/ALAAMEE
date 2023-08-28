##
## File:    simFitPlots.R
## Author:  Alex Stivala
## Created: August 2023
##
## Functions to build goodness-of-fit plots for plotALAAMEESimFit.R
## Adapted from some functions in EstimNetDirected R simFitPlots.R

library(igraph)

library(grid)
library(gridExtra)
library(ggplot2)
library(reshape)
library(doBy)
library(scales)



obscolour <- 'red' # colour to plot observed graph points/lines
## simulated graph statistics will be boxplot on same plot in default colour

ptheme <-  theme(legend.position = 'none')

# http://stackoverflow.com/questions/10762287/how-can-i-format-axis-labels-with-exponents-with-ggplot2-and-scales
orig_scientific_10 <- function(x) {
  parse(text=gsub("e", " %*% 10^", scientific_format()(x)))
}
my_scientific_10 <- function(x) {
# also remove + and leading 0 in exponennt
  parse( text=gsub("e", " %*% 10^", gsub("e[+]0", "e", scientific_format()(x))) )
   
}



##
## Return plot of degree distribution of nodes with outcome 1,
## for in or out degree
##
## Parameters:
##    g_obs:       observed graph igraph object
##    sim_graphs:  simulated graphs list of igraph objects
##    mode:       'in' or 'out' for indegree or outdegree respectively
##                or 'all' for undirected graph
##    btype:      igraph bipartite node type FALSE or TRUE, or NULL
##                if not bipartite. (Default NULL)
##    sim2_graphs if not NULL, simulated graphs from a second model to put on
##                  same plot  for comparison  (default NULL)
##
## Return value:
##    ggplot2 object to add to plot list
##
##
deg_distr_plot <- function(g_obs, sim_graphs, mode, btype=NULL, sim2_graphs=NULL) {
    num_sim <- length(sim_graphs)
    if (!is.null(sim2_graphs)) {
      num_sim2 <- length(sim2_graphs)
      obscolour <- "observed" # for legend
    }
    start = Sys.time()
    if (is.bipartite(g_obs)) {
      maxdeg <- max(unlist(sapply(sim_graphs,
           function(g) degree(g, V(g)[which(V(g)$type == btype & V(g)$outcome == 1)], mode=mode))),
           degree(g_obs, V(g_obs)[which(V(g_obs)$type == btype & V(g)$outcome == 1)], mode=mode))
      if (!is.null(sim2_graphs)) {
        maxdeg<- max(unlist(sapply(sim2_graphs,
                                   function(g) degree(g, V(g)[which(V(g)$type == btype & V(g)$outcome == 1)], mode=mode))),
                     maxdeg)
      }
    } else {
      maxdeg <- max(unlist(sapply(sim_graphs,
                                  function(g) degree(g, V(g)[outcome == 1], mode=mode))),
                    degree(g_obs, V(g_obs)[outcome == 1], mode=mode))
      if (!is.null(sim2_graphs)) {
        maxdeg <- max(unlist(sapply(sim2_graphs,
                                    function(g) degree(g, V(g)[outcome == 1], mode=mode))),
                      maxdeg)
      }
    }
    cat("Max ", mode, " degree is ", maxdeg, "\n")
    deg_df <- data.frame(sim = rep(1:num_sim, each=(maxdeg+1)),
                           degree = rep(0:maxdeg, num_sim),
                           count = NA)
    if (!is.null(sim2_graphs)) {
      deg_df2 <- data.frame(sim = rep(1:num_sim2, each=(maxdeg+1)),
                           degree = rep(0:maxdeg, num_sim2),
                           count = NA)
    }
    end = Sys.time()
    cat(mode, "-degree init took ", as.numeric(difftime(end, start, unit="secs")),"s\n")
    start = Sys.time()
    for (i in 1:num_sim) {
      ## https://stackoverflow.com/questions/1617061/include-levels-of-zero-count-in-result-of-table
      if (is.bipartite(g_obs)) {
        deg_table <- table(factor(degree(sim_graphs[[i]],
    V(sim_graphs[[i]])[which(V(sim_graphs[[i]])$type == btype & V(sim_graphs[[i]])$outcome == 1)], mode = mode),
                                  levels=0:maxdeg))
        if (!is.null(sim2_graphs)) {
          deg_table2 <- table(factor(degree(sim2_graphs[[i]],
                                           V(sim2_graphs[[i]])[which(V(sim2_graphs[[i]])$type == btype & V(sim2_graphs[[i]])$outcome == 1)], mode = mode),
                                    levels=0:maxdeg))
        }
      } else {
        deg_table <- table(factor(degree(sim_graphs[[i]], V(sim_graphs[[i]])[outcome == 1], mode = mode),
                                  levels=0:maxdeg))
        if (!is.null(sim2_graphs)) {
          deg_table2 <- table(factor(degree(sim2_graphs[[i]], V(sim2_graphs[[i]])[outcome == 1], mode = mode),
                                    levels=0:maxdeg))
        }
      }
      deg_df[which(deg_df[,"sim"] == i), "count"] <- deg_table
      if (!is.null(sim2_graphs)) {
        deg_df2[which(deg_df2[,"sim"] == i), "count"] <- deg_table2
      }
    }
    deg_df$degree <- as.factor(deg_df$degree)
    deg_df$count[which(is.na(deg_df$count))] <- 0
    if (!is.null(sim2_graphs)) {
      deg_df2$degree <- as.factor(deg_df2$degree)
      deg_df2$count[which(is.na(deg_df2$count))] <- 0
      }
    if (is.bipartite(g_obs)) {
      deg_df$nodefraction <- deg_df$count / sapply(sim_graphs,
                                 function(g) length(which(V(g)$type == btype & V(g)$outcome == 1)))
      if (!is.null(sim2_graphs)) {
        deg_df2$nodefraction <- deg_df2$count / sapply(sim2_graphs,
                                                     function(g) length(which(V(g)$type == btype & V(g)$outcome == 1)))        
      }
    } else {
      deg_df$nodefraction <- deg_df$count / sapply(sim_graphs, function(g) length(which(V(g)$outcome == 1)))
      if (!is.null(sim2_graphs)) {
        deg_df2$nodefraction <- deg_df2$count / sapply(sim2_graphs, function(g) length(which(V(g)$outcome == 1)))
      }
    }
    end = Sys.time()
    cat(mode, "-degree sim data frame construction took",
        as.numeric(difftime(end, start, unit="secs")), "s\n")
    start = Sys.time()
    obs_deg_df <- data.frame(degree = rep(0:maxdeg),
                               count = NA)
    if (is.bipartite(g_obs)) {
      obs_deg_table <- table(factor(degree(g_obs,
                          V(g_obs)[which(V(g_obs)$type == btype & V(g_obs)$outcome == 1)], mode=mode),
         levels=0:maxdeg))
    } else {
      obs_deg_table <- table(factor(degree(g_obs, V(g_obs)[outcome == 1], mode=mode), levels=0:maxdeg))
    }
    obs_deg_df$count <- as.numeric(obs_deg_table)
    ## without as.numeric() above get error "Error: geom_line requires
    ## the following is.null aesthetics: y" when the plot is finally
    ## printed at the end. Who knows why... even though printing the
    ## data frame and the computations below are apparently not
    ## affected by this at all (does not happen with the boxplot for
    ## simulated degree distribution)
    obs_deg_df$degree <- as.factor(obs_deg_df$degree)
    obs_deg_df$count[which(is.na(obs_deg_df$count))] <- 0
    if (is.bipartite(g_obs)) {
      obs_deg_df$nodefraction <- obs_deg_df$count /
                                         length(which(V(g_obs)$type == btype & V(g_obs)$outcome == 1))
    } else {
      obs_deg_df$nodefraction <- obs_deg_df$count / length(which(V(g_obs)$outcome == 1))
    }
    ##print(obs_deg_df)#XXX
    if (!is.null(sim2_graphs)) {
      deg_df$model <- "Model 1"
      deg_df2$model <- "Model 2"
      deg_df <- rbind(deg_df, deg_df2)
      deg_df$model <- factor(deg_df$model)
    }
    end = Sys.time()
    cat(mode, "-degree obs data frame construction took",
        as.numeric(difftime(end, start, unit="secs")), "s\n")
    start = Sys.time()
    if (!is.null(sim2_graphs)) {
      p <- ggplot(deg_df, aes(x = degree, y = nodefraction, fill = model))
    } else {
      p <- ggplot(deg_df, aes(x = degree, y = nodefraction))
    }
    p <- p + geom_boxplot()
    p <- p + geom_line(data = obs_deg_df, aes(x = degree, y = nodefraction,
                                              colour = obscolour,
                                              group = 1),
                       inherit.aes = FALSE)
    ## the "group=1" is ncessary in the above line otherwise get error
    ## "geom_path: Each group consists of only one observation. Do you
    ## need to adjust the group aesthetic?" and it does not work.
    ## https://stackoverflow.com/questions/27082601/ggplot2-line-chart-gives-geom-path-each-group-consist-of-only-one-observation
    p <- p + ptheme
    if (!is.null(sim2_graphs)) {
      p <- p + theme(legend.title=element_blank(),
                     legend.position = c(0.9, 0.8))
    }
    if (is.bipartite(g_obs)) {
      degreetype <- ifelse(btype, 'mode B degree', 'mode A degree')
    } else {
      degreetype <- 'degree (outcome = 1 nodes)'
    }
    if (mode == 'in' || mode =='out') {
      degreetype <- paste(mode, 'degree (outcome = 1 nodes)', sep='-')
    }
    p <- p + xlab(degreetype) + ylab('fraction of outcome = 1 nodes')
    if (is.bipartite(g_obs)) {
      p <- p + ylab(paste('fraction of outcome = 1 ', ifelse(btype, 'B', 'A'), 'nodes'))
    } else {
      p <- p + ylab('fraction of outcome = 1 nodes')
    }
    if (maxdeg > 200) {
        p <- p + scale_x_discrete(breaks = seq(0, maxdeg, by = 200))
    } else if (maxdeg > 50) {
        p <- p + scale_x_discrete(breaks = seq(0, maxdeg, by = 10))
    } else if (maxdeg > 20) {
        p <- p + scale_x_discrete(breaks = seq(0, maxdeg, by = 5))
    }
    p <- p + guides(x = guide_axis(check.overlap = TRUE))
    end = Sys.time()
    cat(mode, "-degree plotting took",
        as.numeric(difftime(end, start, unit="secs")), "s\n")
    return(p)
}

##
## Return histogram of degree distribution of nodes with outcome 1,
## for in or out degree
##
## Parameters:
##    g_obs:       observed graph igraph object
##    sim_graphs:  simulated graphs list of igraph objects
##    mode:       'in' or 'out' for indegree or outdegree respectively
##                 or all for undirected
##    use_log:    TRUE to do log degree
##    btype:      igraph bipartite node type FALSE or TRUE, or NULL
##                if not bipartite. (Default NULL)
##
## Return value:
##    ggplot2 object to add to plot list
##
deg_hist_plot <- function(g_obs, sim_graphs, mode, use_log, btype=NULL) {
    #print('in deg_hist_plot...')#XXX seems to be only way to debug in R...
    start <- Sys.time()
    if (use_log) {
      if (is.bipartite(g_obs)) {
        dobs <- data.frame(degree = log(degree(g_obs, V(g_obs)[which(V(g_obs)$type == btype & V(g_obs)$outcome == 1)], mode=mode)),
                           group = 'obs')
      } else {
        dobs <- data.frame(degree = log(degree(g_obs, V(g_obs)[outcome == 1], mode=mode)),
                           group = 'obs')
      }        
    } else {
      if (is.bipartite(g_obs)) {
        dobs <- data.frame(degree = degree(g_obs, V(g_obs)[which(V(g_obs)$type == btype & V(g_obs)$outcome ==1)], mode=mode),
                           group = 'obs')
      } else {
        #print('building dobs ...')#XXX seems to be only way to debug in R...
        #print(V(g_obs)$outcome)#XXX seems to be only way to debug in R...
        dobs <- data.frame(degree = degree(g_obs, V(g_obs)[outcome == 1], mode=mode),
                           group = 'obs')
        #print('done building dobs')#XXX seems to be only way to debug in R...
      }          
    }
#    print(names(dobs))#XXX
#    print('about to get simdegrees...')#XXX seems to be only way to debug in R...
  ## get degrees of all simulated graphs in one histogram
  if (is.bipartite(g_obs)) {
    ## as.vector() and unlist() BOTH seems to be required, otherwise rbind() below crashes with error about wrong number of columns
    simdegrees <- as.vector(unlist(sapply(sim_graphs, function(g) degree(g, V(g)[which(V(g)$type == btype & V(g)$outcome == 1)], mode=mode))))
    } else {
      simdegrees <- as.vector(unlist(sapply(sim_graphs, function(g) degree(g, V(g)[outcome == 1], mode=mode))))
    }
    if (use_log) {
        dsim <- data.frame(degree = log(simdegrees), group = 'sim')
    } else {
        dsim <- data.frame(degree = simdegrees, group = 'sim')
    }
#    print(names(dsim))#XXX
#    print('about to rbind dobs and dsim...') #XXX seems to be only way to debug in R...
    dat <- rbind(dobs, dsim)
    end <- Sys.time()
    cat(mode, "-degree histogram data frame construction took",
        as.numeric(difftime(end, start, unit="secs")), "s\n")
    start <- Sys.time()
    ## https://stackoverflow.com/questions/29287614/r-normalize-then-plot-two-histograms-together-in-r
    p <- ggplot(dat, aes(degree, fill = group, colour = group)) +
        geom_histogram(aes(y = ..density..),
                       alpha = 0.4, position = 'identity', lwd = 0.2)
    if (is.bipartite(g_obs)) {
      degreetype <- cat(ifelse(btype, 'mode B degree', 'mode A degree'),
                        '(outcome = 1 nodes)')
    } else {
      degreetype <- 'degree (outcome = 1 nodes)'
    }
    if (mode == 'in' || mode =='out') {
      degreetype <- paste(mode, 'degree (outcome = 1 nodes)', sep='-')
    }
    p <- p + xlab(paste(ifelse(use_log, "log ", ""), degreetype, sep=''))
    p <- p + theme(legend.title=element_blank(),
                   legend.position = c(0.9, 0.8))
    end <- Sys.time()
    cat(mode, "-degree histogram plotting took",
        as.numeric(difftime(end, start, unit="secs")), "s\n")
    return(p)
}



##
## Return list of goodness-of-fit plots
##
## Parameters:
##    g_obs:            observed graph igraph object
##    obs_outcomevec:   observed binary outcome vector
##    sim_outcomevecs:  list or simulated binary outcome vectors
##    sim2_outcomevecs: list of simulated binary outcome vectors from a
##                      different model to compare on same plots
##                      (default NULL)
##
## Return value:
##    list of ggplot2 objects
##
##
build_sim_fit_plots <- function(g_obs, obs_outcomevec, sim_outcomevecs,
                                sim2_outcomevecs = NULL) {

  num_sim <- length(sim_outcomevecs)
  plotlist <- list()


  ## make list of igraph objects with outcome attribute set to that
  ## for each of the simulated outcome vectors (ineffcient, so many
  ## copies of same graph just with different outcome attribute, but
  ## simple) (Can't work out how to "deep copy" igraph graphs in R -
  ## assignment shares the data so modifying one modifies all - so do
  ## it by constructing from edgelist)
  sim_graphs <- rep(list(graph_from_edgelist(as_edgelist(g_obs))), num_sim)
  for (i in 1:length(sim_graphs)) {
    V(sim_graphs[[i]])$outcome <- sim_outcomevecs[[i]]
  }
  if (!is.null(sim2_outcomevecs)) {
    num_sim2 <- length(sim2_outcomevecs)
    sim2_graphs <- rep(list(graph_from_edgelist(as_edgelist(g_obs))), num_sim2)
    for (i in 1:length(sim2_graphs)) {
      V(sim2_graphs[[i]])$outcome <- sim2_outcomevecs[[i]]
    }
  } else {
    sim2_graphs <- NULL
  }


  if (is.directed(g_obs)) {
    ##
    ## In degree
    ##

    system.time(plotlist <- c(plotlist,
                              list(deg_distr_plot(g_obs, sim_graphs, 'in',
                                                  sim2_graphs=sim2_graphs))))

    if (is.null(sim2_graphs)) {
      system.time(plotlist <- c(plotlist,
                                list(deg_hist_plot(g_obs, sim_graphs, 'in', FALSE))))
      
      system.time(plotlist <- c(plotlist,
                                list(deg_hist_plot(g_obs, sim_graphs, 'in', TRUE))))
    }


    ##
    ## Out degree
    ##

    system.time(plotlist <- c(plotlist,
                              list(deg_distr_plot(g_obs, sim_graphs, 'out', sim2_graphs=sim2_graphs))))

    if (is.null(sim2_graphs)) {
      system.time(plotlist <- c(plotlist,
                                list(deg_hist_plot(g_obs, sim_graphs, 'out', FALSE))))
      
      system.time(plotlist <- c(plotlist,
                                list(deg_hist_plot(g_obs, sim_graphs, 'out', TRUE))))
    }

  } else {
    ##
    ## Degree
    ##

    if (is.bipartite(g_obs)) {
      system.time(plotlist <- c(plotlist,
                                list(deg_distr_plot(g_obs, sim_graphs,
                                                    'all', FALSE, sim2_graphs=sim2_graphs))))
      system.time(plotlist <- c(plotlist,
                                list(deg_distr_plot(g_obs, sim_graphs,
                                                    'all', TRUE, sim2_graphs=sim2_graphs))))      
    } else {
      system.time(plotlist <- c(plotlist,
                                list(deg_distr_plot(g_obs, sim_graphs, 'all', sim2_graphs=sim2_graphs))))
    }

    if (is.null(sim2_graphs)) {
      if (is.bipartite(g_obs)) {
        system.time(plotlist <- c(plotlist,
                                  list(deg_hist_plot(g_obs, sim_graphs, 'all', FALSE, FALSE))))
        
        system.time(plotlist <- c(plotlist,
                                  list(deg_hist_plot(g_obs, sim_graphs, 'all', TRUE, FALSE))))
        system.time(plotlist <- c(plotlist,
                                  list(deg_hist_plot(g_obs, sim_graphs, 'all', FALSE, TRUE))))
        
        system.time(plotlist <- c(plotlist,
                                  list(deg_hist_plot(g_obs, sim_graphs, 'all', TRUE, TRUE))))
      } else {
        system.time(plotlist <- c(plotlist,
                                  list(deg_hist_plot(g_obs, sim_graphs, 'all', FALSE))))
        
        system.time(plotlist <- c(plotlist,
                                  list(deg_hist_plot(g_obs, sim_graphs, 'all', TRUE))))
      }
    }
  }



  return(plotlist)
}
