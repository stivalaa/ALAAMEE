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
library(RColorBrewer)

## read in R source file from directory where this script is located
##http://stackoverflow.com/questions/1815606/rscript-determine-path-of-the-executing-script
source_local <- function(fname){
  argv <- commandArgs(trailingOnly = FALSE)
  base_dir <- dirname(substring(argv[grep("--file=", argv)], 8))
  source(paste(base_dir, fname, sep=.Platform$file.sep))
}

source_local('EIindex.R')


## Change default font size to make it larger so readable when included in
## LaTeX documents and reduced in smaller panels
## https://ggplot2.tidyverse.org/articles/faq-customising.html

theme_set(theme_gray(base_size = 14))

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
##    model_names - two-element vector of model names, corresponding to
##                  sim_graphs and sim2_graphs (default c("Model 1", "Model 2"))
##
## Return value:
##    ggplot2 object to add to plot list
##
##
deg_distr_plot <- function(g_obs, sim_graphs, mode, btype=NULL, sim2_graphs=NULL, model_names = c("Model 1", "Model 2")) {
  
    num_sim <- length(sim_graphs)
    if (!is.null(sim2_graphs)) {
      num_sim2 <- length(sim2_graphs)
      obscolour <- "observed" # for legend
      palette_name = "Dark2" # RColorBrewer palette name
    } else {
      palette_name = "Set1"
    }
    start = Sys.time()
    if (is.bipartite(g_obs)) {
       if (length(which(V(g_obs)$type == btype & V(g_obs)$outcome == 1)) == 0) {
         cat("No nodes with outcome 1 in btype ", btype, ", skipping\n")
         return(list()) #empty list element
       }
      maxdeg <- max(unlist(sapply(sim_graphs,
           function(g) degree(g, V(g)[which(V(g)$type == btype & V(g)$outcome == 1)], mode=mode))),
           degree(g_obs, V(g_obs)[which(V(g_obs)$type == btype & V(g_obs)$outcome == 1)], mode=mode))
      meandeg_sim <- mean(unlist(sapply(sim_graphs,
           function(g) degree(g, V(g)[which(V(g)$type == btype & V(g)$outcome == 1)], mode=mode))))
      meandeg_obs <- mean(degree(g_obs, V(g_obs)[which(V(g_obs)$type == btype & V(g_obs)$outcome == 1)], mode=mode))
      if (!is.null(sim2_graphs)) {
        maxdeg<- max(unlist(sapply(sim2_graphs,
                                   function(g) degree(g, V(g)[which(V(g)$type == btype & V(g)$outcome == 1)], mode=mode))),
                     maxdeg)
        meandeg_sim2 <- mean(unlist(sapply(sim2_graphs,
                          function(g) degree(g, V(g)[which(V(g)$type == btype & V(g)$outcome == 1)], mode=mode))))
        #print(unlist(sapply(sim2_graphs, function(g) degree(g, V(g)[which(V(g)$type == btype & V(g)$outcome == 1)], mode=mode)))) #XXX
        cat('meandeg_sim2 = ', meandeg_sim2, '\n')
      }
    } else {
      maxdeg <- max(unlist(sapply(sim_graphs,
                                  function(g) degree(g, V(g)[outcome == 1], mode=mode))),
                    degree(g_obs, V(g_obs)[outcome == 1], mode=mode))
      meandeg_sim <- mean(unlist(sapply(sim_graphs,
                  function(g) degree(g, V(g)[outcome == 1], mode=mode))))
      meandeg_obs <- mean(degree(g_obs, V(g_obs)[outcome == 1], mode=mode))
      if (!is.null(sim2_graphs)) {
        maxdeg <- max(unlist(sapply(sim2_graphs,
                                    function(g) degree(g, V(g)[outcome == 1], mode=mode))),
                      maxdeg)
        meandeg_sim2 <- mean(unlist(sapply(sim2_graphs,
                                    function(g) degree(g, V(g)[outcome == 1], mode=mode))))
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
      deg_df$model <- model_names[1]
      deg_df2$model <- model_names[2]
      deg_df <- rbind(deg_df, deg_df2)
      deg_df$model <- factor(deg_df$model)
      ## https://stackoverflow.com/questions/6919025/how-to-assign-colors-to-categorical-variables-in-ggplot2-that-have-stable-mappin
      palette <- brewer.pal(3, palette_name)
      myColors <- palette[2:3] # force only two colors
      names(myColors) <- levels(deg_df$model)
      colScale <- scale_fill_manual(name = "model", values = myColors)
    }
    end = Sys.time()
    cat(mode, "-degree obs data frame construction took",
        as.numeric(difftime(end, start, unit="secs")), "s\n")
    stopifnot(all(!is.na(deg_df$model)))
    start = Sys.time()
    if (!is.null(sim2_graphs)) {
      p <- ggplot(deg_df, aes(x = degree, y = nodefraction, fill = model))
      p <- p + colScale
    } else {
      p <- ggplot(deg_df, aes(x = degree, y = nodefraction))
    }
    p <- p + geom_boxplot()
    p <- p + geom_line(data = obs_deg_df, aes(x = degree, y = nodefraction,
                                              colour = obscolour,
                                              group = 1),
                       inherit.aes = FALSE) +
      scale_colour_brewer(palette = palette_name)
    p <- p + geom_point(data = obs_deg_df, aes(x = degree, y = nodefraction,
                                              colour = obscolour,
                                              group = 1),
                        inherit.aes = FALSE) +
      scale_colour_brewer(palette = palette_name)
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
    p <- p + xlab(degreetype) + ylab('frac. outcome = 1 nodes')
    if (is.bipartite(g_obs)) {
      p <- p + ylab(paste('frac. outcome = 1 ', ifelse(btype, 'B', 'A'), 'nodes'))
    } else {
      p <- p + ylab('frac. outcome = 1 nodes')
    }
    if (maxdeg > 200) {
        p <- p + scale_x_discrete(breaks = seq(0, maxdeg, by = 200))
    } else if (maxdeg > 50) {
        p <- p + scale_x_discrete(breaks = seq(0, maxdeg, by = 10))
    } else if (maxdeg > 20) {
        p <- p + scale_x_discrete(breaks = seq(0, maxdeg, by = 5))
    }
    p <- p + guides(x = guide_axis(check.overlap = TRUE))

    if (!is.null(sim2_graphs)) {
      p <- p + geom_vline(xintercept = meandeg_sim, linetype = "dashed", color = myColors[1])
      p <- p + geom_vline(xintercept = meandeg_sim2, linetype = "dashed",color = myColors[2])
      p <- p + geom_vline(xintercept = meandeg_obs, linetype = "solid",color = palette[1])
    }
    
    end = Sys.time()
    cat(mode, "-degree plotting took",
        as.numeric(difftime(end, start, unit="secs")), "s\n")
    warnings()
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
    if (is.bipartite(g_obs)) {
       if (length(which(V(g_obs)$type == btype & V(g_obs)$outcome == 1)) == 0) {
         cat("(deg_hist_plot) No nodes with outcome 1 in btype ", btype, ", skipping\n")
         return(list()) #empty list element
       }
    }
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
    #cat('XXX',mode,btype,'\n')
    ## as.vector() and unlist() BOTH seems to be required, otherwise rbind() below crashes with error about wrong number of columns
   #print(sim_graphs)#XXX
    simdegrees <- as.vector(unlist(sapply(sim_graphs, function(g) degree(g, V(g)[which(V(g)$type == btype & V(g)$outcome == 1)], mode=mode))))
    #print(simdegrees)#XXX
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
      degreetype <- paste(ifelse(btype, 'mode B degree', 'mode A degree'),
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
##    model_names - two-element vector of model names, corresponding to
##                  sim_graphs and sim2_graphs (default c("Model 1", "Model 2"))
##    outdegree_only - if TRUE then only do out-degree distribution not
##                    in-degree for directed graphs (default FALSE).
##    do_assortativity - if TRUE then do assortativity on outcome attribute
##                       (default FALSE)
##    do_eiindex - if TRUE then do E-I index on outcome attribute
##                       (default FALSE)
##
## Return value:
##    list of ggplot2 objects
##
##
build_sim_fit_plots <- function(g_obs, obs_outcomevec, sim_outcomevecs,
                                sim2_outcomevecs = NULL,
                                model_names = c("Model 1", "Model 2"),
                                outdegree_only = FALSE,
                                do_assortativity = FALSE,
                                do_eiindex = FALSE) {

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
    ## for bipartite graphs, we also have to reconstruct the node type
    if (is.bipartite(g_obs)) {
      V(sim_graphs[[i]])$type <- V(g_obs)$type
    }
  }
  if (!is.null(sim2_outcomevecs)) {
    num_sim2 <- length(sim2_outcomevecs)
    sim2_graphs <- rep(list(graph_from_edgelist(as_edgelist(g_obs))), num_sim2)
    for (i in 1:length(sim2_graphs)) {
      V(sim2_graphs[[i]])$outcome <- sim2_outcomevecs[[i]]
      ## for bipartite graphs, we also have to reconstruct the node type
      if (is.bipartite(g_obs)) {
        V(sim2_graphs[[i]])$type <- V(g_obs)$type
      }
    }
  } else {
    sim2_graphs <- NULL
  }


  if (is.directed(g_obs)) {
    ##
    ## In degree
    ##
    if (!outdegree_only) {
      system.time(plotlist <- c(plotlist,
                                list(deg_distr_plot(g_obs, sim_graphs, 'in',
                                                    sim2_graphs=sim2_graphs,
                                                    model_names = model_names))))
      
      if (is.null(sim2_graphs)) {
        system.time(plotlist <- c(plotlist,
                                  list(deg_hist_plot(g_obs, sim_graphs, 'in', FALSE))))
        
        system.time(plotlist <- c(plotlist,
                                  list(deg_hist_plot(g_obs, sim_graphs, 'in', TRUE))))
      }
    }


    ##
    ## Out degree
    ##

    system.time(plotlist <- c(plotlist,
                              list(deg_distr_plot(g_obs, sim_graphs, 'out', sim2_graphs=sim2_graphs, model_names=model_names))))

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
                                                    'all', FALSE, sim2_graphs=sim2_graphs, model_names=model_names))))
      system.time(plotlist <- c(plotlist,
                                list(deg_distr_plot(g_obs, sim_graphs,
                                                    'all', TRUE, sim2_graphs=sim2_graphs, model_names=model_names))))      
    } else {
      system.time(plotlist <- c(plotlist,
                                list(deg_distr_plot(g_obs, sim_graphs, 'all', sim2_graphs=sim2_graphs, model_names=model_names))))
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

  ##
  ## Assortitivity on outcome attribute
  ##
  if (do_assortativity) {
    ## Note in igraph assortativity.nominal() the types must start at 1 not 0
    system.time( obs_assortativity <- assortativity.nominal(g_obs, 1+V(g_obs)$outcome) )
    system.time( sim_assortativity <- sapply(sim_graphs, function(g) assortativity.nominal(g, 1+V(g)$outcome)) )
    cat('obs assortativity: ', obs_assortativity, '\n')
    cat('sim assortativity: ', sim_assortativity, '\n')
    p <- ggplot() + geom_boxplot(aes(x = 'outcome', y = sim_assortativity))
    p <- p + geom_point(aes(x = as.numeric(ordered('outcome')),
                            y = obs_assortativity,
                            colour = obscolour))
    p <- p + ylab('assortativity') + ptheme +
      theme(axis.title.x = element_blank())
    ##p <- p + ylim(0, 1)
    plotlist <- c(plotlist, list(p))
  }

  ##
  ## E-I index on outcome attribute
  ##
  if (do_eiindex) {
    system.time( obs_eiindex <- EIindex(g_obs, "outcome") )
    system.time( sim_eiindex <- sapply(sim_graphs, function(g) EIindex(g, "outcome")) )
    cat('obs eiindex: ', obs_eiindex, '\n')
    cat('sim eiindex: ', sim_eiindex, '\n')
    p <- ggplot() + geom_boxplot(aes(x = 'outcome', y = sim_eiindex))
    p <- p + geom_point(aes(x = as.numeric(ordered('outcome')),
                            y = obs_eiindex,
                            colour = obscolour))
    p <- p + ylab('E-I index') + ptheme +
      theme(axis.title.x = element_blank())
    ##p <- p + ylim(0, 1)
    plotlist <- c(plotlist, list(p))
  }


  ## remove empty elements
  plotlist <- plotlist[lapply(plotlist, length) > 0]
  return(plotlist)
}
