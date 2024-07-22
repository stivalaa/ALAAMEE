#!/usr/bin/Rscript
##
## File:    makeMLEresultsTableVarTotalRuns.R
## Author:  Alex Stivala
## Created: May 2023
##
##
## Read estimation results from
## build_alaamee_estimation_var_total_runs_results_tab.sh
## and make table of estimates and standard errors and false negative rates.
##
## Usage: Rscript [-s] makeMLEresultsTableVarTotalRuns.R results_filename
##
## Output is to stdout
##
## e.g.: Rscript makeMLEresultsTableVarTotalRuns.R alaamee_estimates_var_total_runs_simulated_Project90.txt
## 

library(PropCIs) # for Wilson score test for false negative rate

#zSigma <- 1.96 # number of standard deviations for 95% confidence interval
#zSigma <- 2.58 # number of standard deviations for 99% confidence interval
zSigma <- 2 # nominal 95% CI


options(digits=4) # for printing rmse etc. values



args <- commandArgs(trailingOnly=TRUE)
use_sd_theta <- FALSE
if (length(args) > 1 ) {
   if (args[1] == "-s") {
      use_sd_theta <- TRUE
    }
    results_filenames <- args[2]
} else {
  results_filenames <- args[1]
}

## write header line
cat("N Descr ErrorAnalysis FixedDensity Effect Bias RMSE FNRpercent MeanStdErr StdDevEstimate NumConverged FNRpercentLower FNRpercentUpper TotalNetworksConverged TotalRuns PercentInCI\n")

for (results_filename in results_filenames) {
  Dorig <- read.table(results_filename, header=TRUE, stringsAsFactors=TRUE)
  
  ## Project 90 simulated ALAAM parameters as used in Stivala et al (2020)
  ## arXiv:2002.00849v2 (ALAAM snowball paper) harcoded here
  
  effects <- c('Density', 'Activity', 'Contagion', 'binary_oOb', 'continuous_oOc')

  ## output effect names, corresponding to above
  effect_names <- c('Density', 'Activity', 'Contagion', 'Binary', 'Continuous')

  ## known true values of effects above (for drawing horizontal line on plot)
  true_parameters <- c(-15.0, 0.55, 1.00, 1.20, 1.15)

  error_analysis <- 'ALAAMEE'
  fixeddensity <- 'N'
  network_N_list <- 4430
  attribute_descr <- 'Project90simulated'
  totalRuns_list <- unique(Dorig$totalRuns)
  
  for (network_N in network_N_list) {
    for (this_totalRuns in totalRuns_list) {
      if ('nodeCount' %in% names(Dorig)) {
        D <- Dorig[which(Dorig$nodeCount == network_N), ]
      }  else {
        D <- Dorig
      }

      D <- Dorig[which(Dorig$totalRuns == this_totalRuns), ]

      if (use_sd_theta) {
        D$StdErr <- D$sdEstimate ## Use sd(theta) as estimated standard eror
      }

      if (length(grep('binattr', results_filename)) > 0) {
        attribute_descr <- 'Binary' 
      }
      else if (length(grep('cat3', results_filename)) > 0) {
        attribute_descr <- 'Categorical'
      }
      else if (length(grep('cont', results_filename)) > 0) {
        attribute_descr <- 'Continuous'
      }


      this_effects <- effects
      this_true_parameters <- true_parameters

      for (i in 1:length(this_effects)) {
        effect <- this_effects[i]
        De <- D[which(D$Effect == effect),]
        if (length(De$Effect) == 0) {
          next
        }
        

        ## remove unconverged samples 
        if ('t.ratio' %in% names(De)) {
          oldn <- nrow(De)
          De <- De[which(De$t.ratio <= 0.1), ]
          if (nrow(De) != oldn) {
            write(paste('removed',oldn-nrow(De),'unconverged estimates'),stderr())
          }
        }

        ## remove samples with NaN or infinite Estimate
        De <- De[which(!is.na(De$Estimate)), ]
        De <- De[which(!is.infinite(De$Estimate)),]
        De <- De[which(abs(De$Estimate) < 1e03),] ## sometimes not inf but still huge
        ## remove samples with zero or extreme values as StdErr 
        ## De <- De[which(De$StdErr != 0),]
        ## De <- De[which(!is.na(De$StdErr)),]
        ## De <- De[which(!is.infinite(De$StdErr)),]
        ## De <- De[which(De$StdErr < 1e10),]


        totalRuns <- unique(De$totalRuns)
        stopifnot(length(totalRuns) == 1)
        

        rmse <- sqrt(mean((De$Estimate - this_true_parameters[i])^2))
        bias <- mean(De$Estimate - this_true_parameters[i])

        ## count number of times the CI  includes true value
        num_in_ci <- sum((De$Estimate < this_true_parameters[i] & De$Estimate + zSigma*De$StdErr >= this_true_parameters[i]) | (De$Estimate >= this_true_parameters[i] & De$Estimate - zSigma*De$StdErr <= this_true_parameters[i]))
        perc_in_ci <- 100 * num_in_ci / length(De$Estimate)

        num_samples <- length(unique(De$sampleId))
        cat("totalRuns = ", totalRuns, ", effect = ", effect, ", length(De$Estimate) = ", length(De$Estimate), ", num_samples = ", num_samples, "\n", file=stderr())#XXX
        
        ## for purely inference (sign and significance, not actual value of estimate)
        ## compute False Negative rate, as the number of times the estimate
        ## is the right sign, but the CI includes zero; or, is the wrong sign.
        
        false_negative_count <-
          sum( (sign(De$Estimate) == sign(this_true_parameters[i]) & 
                ((De$Estimate < 0 & De$Estimate + zSigma*De$StdErr >= 0) |
                 (De$Estimate >= 0 & De$Estimate - zSigma*De$StdErr <= 0)) ) |
               sign(De$Estimate) != sign(this_true_parameters[i]) )
        false_negative_perc <- 100 * false_negative_count / length(De$Estimate)
        confint <- scoreci(false_negative_count, length(De$Estimate), 0.95)
        fnp_lower <- confint$conf.int[1] * 100
        fnp_upper <- confint$conf.int[2] * 100
        cat(network_N, attribute_descr, error_analysis, fixeddensity, 
            effect, bias, rmse, false_negative_perc,
            mean(De$StdErr), sd(De$Estimate), mean(De$convergedRuns),
            fnp_lower, fnp_upper,
            length(De$Estimate), totalRuns, perc_in_ci)
        cat('\n')
      }
    }
  }
}

