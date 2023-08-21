##
## File:    plot_mean_and_variance.R
## Author:  Alex Stivala
## Created: July 2023
##
## Function to do plots showing phase transition (near-degeneracy) behaviour in
## ALAAM models on different networks. Similar to plots show this behaviour
## in ERGM with Markov random graphs in Fig. 6.5 and 6.6 in 
##
##   Lusher, D., Koskinen, J., & Robins, G. (Eds.). (2013). Exponential random
##   graph models for social networks: Theory, methods, and applications.
##   Cambridge University Press.
##
## Or more closely, in the ALAAM case, being a Markov Random Field,
## for the Ising model as in e.g. Fig. 2 in
##
##   Stoehr, J. (2017). A review on statistical inference methods for
##   discrete Markov random fields. arXiv preprint arXiv:1704.03331.
##


library(ggplot2)
library(scales)

# http://stackoverflow.com/questions/10762287/how-can-i-format-axis-labels-with-exponents-with-ggplot2-and-scales
orig_scientific_10 <- function(x) {
  parse(text=gsub("e", " %*% 10^", scientific_format()(x)))
}
my_scientific_10 <- function(x) {
# also remove + and leading 0 in exponennt
  parse( text=gsub("e", " %*% 10^", gsub("e[+]0", "e", scientific_format()(x))) )
}

## Change default font size to make it larger so readable when included in
## LaTeX documents and reduced in smaller panels
## https://ggplot2.tidyverse.org/articles/faq-customising.html

theme_set(theme_gray(base_size = 28))

###
### plot_mean_and_variances() - make plots of mean and variance of a statistic
###
### Parameters:
###    varname          - name of parameter that is varied for x axis
###                       e.g. "Contagion" or "Activity". Note "theta_"
###                       is prepended to this got get e.g. "theta_Contagion"
###                       as used in the data read in.
###    statname         - name of statistic used as order parameter (y axis)
##3                       e.g. "Contagion" or "Density"
###    outfile_basename - base filename of output files
###                       e.g. "project90"
###    obs              - optional, if present data frame with one row, 
###                       and column for varname e.g. "Contagion",
###                       the observed statistic
###                       value to plot horizontal line on mean and scatterplot
###
## Writes outfile_basename__varname_statname_var.eps and
## outfile_basename_varname_statname_mean.eps and
## outfile_basename_varname_statname_scatterplot in cwd.
###
plot_mean_and_variance <- function(varname, statname, outfile_basename, obs) {
  outfile_var <- paste(outfile_basename, "_", varname, "_", statname, "_var.eps", sep="")
  outfile_mean  <- paste(outfile_basename, "_", varname, "_", statname, "_mean.eps", sep="")
  outfile_scatterplot  <- paste(outfile_basename, "_", varname, "_", statname, "_scatterplot.eps", sep="")

  cat(outfile_mean, "\n")
  postscript(outfile_mean)
  p <- ggplot(dat, aes_string(x = paste("theta_", varname, sep=""),
                              y = statname)) +
    stat_summary(geom = "line", fun = mean) +
    xlab(bquote(theta[.(varname)])) +
    scale_y_continuous(labels = my_scientific_10)
  if (!missing(obs)) {
    p <- p + geom_hline(yintercept = obs[1, varname],
                        linetype= "dashed", color = "red")
  }
  print(p)
  dev.off()

  cat(outfile_var, "\n")
  postscript(outfile_var)
  p <- ggplot(dat, aes_string(x = paste("theta_", varname, sep=""),
                              y = statname)) +
    stat_summary(geom = "line", fun = var) +
    xlab(bquote(theta[.(varname)])) +
    ylab(paste("Var(", statname, ")", sep="")) +
    scale_y_continuous(labels = my_scientific_10)
  print(p)
  dev.off()

  cat(outfile_scatterplot, "\n")
  postscript(outfile_scatterplot)
  p <- ggplot(dat, aes_string(x = paste("theta_", varname, sep=""),
                              y = statname)) +
    geom_point() +
    xlab(bquote(theta[.(varname)])) +
    scale_y_continuous(labels = my_scientific_10)
  if (!missing(obs)) {
    p <- p + geom_hline(yintercept = obs[1, varname],
                        linetype= "dashed", color = "red")
  }
  print(p)
  dev.off()
}
