#!/usr/bin/Rscript
#
# File:    plotMLEresultsFalsePositivesVarTotalRuns.R
# Author:  Alex Stivala
# Created: May 2023
#
#
#
# Read error statistics results from makeMLEresultstableVarTotalRuns.R
# and plot false positive rate against number of runs in meta-analysis.
#
# Usage: Rscript plotMLEresultsFalsePositivesVarTotalRuns.R estimator_error_false_positive_statistics_var_total_runs.txt
#
#
# Output files are PostScript files named
#
#  basename.eps
#
# where basenanme is basename of estimator_error_false_positive_statistics_var_total_runs.txt
#
# e.g.: Rscript plotMLEresultsFalsePositivesVarTotalRuns.R estimator_error_false_positive_statistics_var_total_runs.txt
# 

library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
results_filename <- args[1]
basefilename <- sub("(.+)[.].+", "\\1", basename(results_filename))


effects <- c('Activity', 'Contagion', 'binary_oOb', 'continuous_oOc')

# output effect names, corresponding to above
effect_names <- c('Activity', 'Contagion', 'Binary', 'Continuous')

 
D <- read.table(results_filename, header=TRUE, stringsAsFactors=TRUE)

# remove density as no data for zero density
D <- D[which(D$Effect != "Density"), ]

p <- ggplot(D, aes(x = TotalRuns, y = FPRpercent))
p <- p + theme_bw()
p <- p + theme(panel.background = element_blank(),
               ## panel.grid.major = element_blank(),
               ## panel.grid.minor = element_blank(),
               plot.background = element_blank(),
               strip.background = element_blank(),
               legend.text = 	element_text(size = 10, colour = "black"),
               legend.key =  	element_rect(fill = "white", colour = "white"),
               panel.border = element_rect(color = 'black')
               )
p <- p + ylim(c(0, 100))
p <- p + geom_point()
p <- p + geom_errorbar(aes(ymax = FPRpercentUpper, ymin = FPRpercentLower))
p <- p + xlab("Total runs per sample")
p <- p + ylab("False positive rate (%)")
p <- p + facet_grid(factor(Effect, levels = effects, labels = effect_names) ~ .)

postscript(paste(basefilename, '.eps', sep=''), onefile=FALSE,
           paper="special", horizontal=FALSE, width=9, height=6)
print(p)
dev.off()
