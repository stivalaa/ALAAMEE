#!/usr/bin/Rscript
#
# File:    makeMLEresultstableFalsePositivesVarTotalRuns.R
# Author:  Alex Stivala
# Created: May 2023
#
#
# Read estimation results from
# build_alaamee_estimation_var_total_runs_results_tab.sh
# and make table of estimates and standard errors and false positive rates.
#
#
# Usage: Rscript makeMLEresultstableFalsePositivesVarTotalRuns.R reults_filenames_prefix
#
#
# Output is to stdout
#
# e.g.: Rscript makeMLEresultstableFalsePositivesVarTotalRuns.R alaamee_estimates_var_total_runs_simulated_Project90_
# 

library(PropCIs) # for Wilson score test for false positive rate


#zSigma <- 1.96 # number of standard deviations for 95% confidence interval
#zSigma <- 2.58 # number of standard deviations for 99% confidence interval
zSigma <- 2 # nominal 95% CI


options(digits=4) # for printing rmse etc. values


args <- commandArgs(trailingOnly=TRUE)
prefix <- args[1]

results_filenames <- c(paste(prefix, 'activity0.txt', sep=''),
                       paste(prefix, 'contagion0.txt', sep=''),
                       paste(prefix, 'binary0.txt', sep=''),
                       paste(prefix, 'continuous0.txt', sep=''))
 

# write header line
cat("N Descr ErrorAnalysis FixedDensity Effect ZeroEffect Bias RMSE FPRpercent MeanStdErr StdDevEstimate NumConverged FPRpercentLower FPRpercentUpper TotalNetworksConverged TotalRuns PercentInCI\n")

for (results_filename in results_filenames) {

    # Project 90 simulated ALAAM parameters as used in Stivala et al (2020)
    # arXiv:2002.00849v2 (ALAAM snowball paper) harcoded here
          
    effects <- c('Density', 'Activity', 'Contagion', 'binary_oOb', 'continuous_oOc')

    # output effect names, corresponding to above
    effect_names <- c('Density', 'Activity', 'Contagion', 'Binary', 'Continuous')

    # known true values of effects above (for drawing horizontal line on plot)
    true_parameters <- c(-15.0, 0.55, 1.00, 1.20, 1.15)

    error_analysis <- 'ALAAMEE'
    fixeddensity <- 'N'
    network_N <- 4430
    attribute_descr <- 'Project90simulated'
     
    Dorig <- read.table(results_filename, header=TRUE, stringsAsFactors=TRUE)

      zero_effect <- "*UNKNOWN*" # should always be replced with a valid name
                
      # use filename to see if data had one of the parameters set to zero
      if (length(grep("_activity0", results_filename)) > 0) {
        true_parameters[1] <- -7.0 # For Activity=0 density is -7.0 not -15.0
        true_parameters[2] <- 0.0
        zero_effect <- effects[2]
      }
      if (length(grep("_contagion0", results_filename)) > 0) {
        true_parameters[3] <- 0.0
        zero_effect <- effects[3]
      }
      if (length(grep("_binary0", results_filename)) > 0) {
        true_parameters[4] <- 0.0
        zero_effect <- effects[4]
      }
      if (length(grep("_continuous0", results_filename)) > 0) {
        true_parameters[5] <- 0.0
        zero_effect <- effects[5]
      }

      totalRuns_list <- unique(Dorig$totalRuns)

      for (this_totalRuns in totalRuns_list) {

          D <- Dorig[which(Dorig$totalRuns == this_totalRuns), ]

          for (i in 1:length(effects)) {
                    effect <- effects[i]
                    De <- D[which(D$Effect == effect),]

                    if (length(De$Effect) == 0) {
                                    next
                    }

                    # remove samples with NaN or infinite Estimate
                    De <- De[which(!is.na(De$Estimate)), ]
                    De <- De[which(!is.infinite(De$Estimate)),]
                    De <- De[which(abs(De$Estimate) < 1e03 ),] # sometimes not inf but still huge
                    # remove samples with zero or extreme values as StdErr 
                    ## De <- De[which(De$StdErr != 0),]
                    ## De <- De[which(!is.na(De$StdErr)),]
                    ## De <- De[which(!is.infinite(De$StdErr)),]
                    ## De <- De[which(De$StdErr < 1e10),]

                    if (length(De$Effect) == 0) {
                        cat("Removed all estimates for", effect,"\n",file=stderr())
                        cat(network_N, attribute_descr, error_analysis, fixeddensity, 
                            effect, zero_effect,
                            'NaN', 'NaN', 'NaN',#bias, rmse, false_positive_perc,
                            'NaN','NaN',#mean(De$StdErr), sd(De$Estimate),
                            mean(De$convergedRuns),
                            'NaN','NaN', #fpp_lower, fpp_upper,
                            length(De$Estimate), totalRuns,
                            'NaN' # % in CI
                          )
                        cat('\n')
                        
                        next
                    }
                    
                    totalRuns <- unique(De$totalRuns)
                    stopifnot(length(totalRuns) == 1)
        

                    rmse <- sqrt(mean((De$Estimate - true_parameters[i])^2))
                    bias <- mean(De$Estimate - true_parameters[i])

                    # count number of times the CI (zSigma std errors) includes true value
                    num_in_ci <- sum((De$Estimate < true_parameters[i] & De$Estimate + zSigma*De$StdErr >= true_parameters[i]) | (De$Estimate >= true_parameters[i] & De$Estimate - zSigma*De$StdErr <= true_parameters[i]))
                    perc_in_ci <- 100 * num_in_ci / length(De$Estimate)

                    # for purely inference (sign and significance, not actual
                    # value of estimate) compute False Postivie rate, as the
                    # number of times the estimate CI does not include zero
                    if (zero_effect == effect) {
                        stopifnot(true_parameters[i] == 0.0)
                        false_positive_count <- sum(
                            (De$Estimate < 0 & De$Estimate + zSigma*De$StdErr < 0) |
                            (De$Estimate > 0 & De$Estimate - zSigma*De$StdErr > 0) )
                        false_positive_perc <- 100 * false_positive_count / length(De$Estimate)
                        confint <- scoreci(false_positive_count, length(De$Estimate), 0.95)
                        fpp_lower <- confint$conf.int[1] * 100
                        fpp_upper <- confint$conf.int[2] * 100

                    }
                    else {
                        false_positive_perc <- NA
                        fpp_lower <- NA
                        fpp_upper <- NA
                    }


                    ## print(results_filename)#xxx
                    ## print(effect)#xxx
                    ## print(zero_effect)#xxx
                    ## print(De$N)#xxx

                    cat(network_N, attribute_descr, error_analysis, fixeddensity, 
                        effect, zero_effect,
                        bias, rmse, false_positive_perc,
                        mean(De$StdErr), sd(De$Estimate), mean(De$convergedRuns),
                        fpp_lower, fpp_upper, 
                        length(De$Estimate), totalRuns, perc_in_ci
                       )
                    cat('\n')
		}

         }
}

