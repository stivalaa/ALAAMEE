#!/usr/bin/Rscript
#
# File:    makeMLEresultstableFalsePositives.R
# Author:  Alex Stivala
# Created: December 2013
#
#
#
# Read snowball sampling results (from buildresults.sh) and make table
# of snowball estimates and standard errors.
# This version, unlike makeMLEresultstable.R, handles the simulated
# networks each with one effect set to zero, to identifify false positvies
# in the inference (rather than false negatives).
#
# Usage: Rscript makeMLEresultstableFalsePositives.R  results_filename_prefix
#
#
# Output is to stdout
#
# e.g.: Rscript makeMLEresultstableFalsePositives.R alaamee_estimates_simulated_Project90_
# 

library(PropCIs) # for Wilson score test for false negative rate


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

 
args <- commandArgs(trailingOnly=TRUE)
use_sd_theta <- FALSE
if (length(args) > 0 ) {
   if (args[1] == "-s") {
      use_sd_theta <- TRUE
    }
}  

# now only write the rows, use shell script to sort and add header

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
    num_seedsets <- NA
     
    D <- read.table(results_filename, header=TRUE, stringsAsFactors=TRUE)

    if (use_sd_theta) {
      D$StdErr <- D$sdEstimate # Use sd(theta) as estimated standard eror
    }
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
                            gsub('_', ' ', effect), sub('_', ' ', zero_effect),
                            'NaN', 'NaN', 'NaN',#bias, rmse, false_positive_perc,
                            'NaN','NaN',#mean(De$StdErr), sd(De$Estimate),
                            mean(De$convergedRuns),
                            'NaN','NaN', #fpp_lower, fpp_upper,
                            num_seedsets,
                            length(De$Estimate), totalRuns,
                            'NaN', # % in CI
                            sep=' & ')
                        cat('\\\\\n')
                        
                        next
                    }
                    
                    totalRuns <- unique(De$totalRuns)
                    stopifnot(length(totalRuns) == 1)
        

                    if (effect == "R_Attribute1"  && substr(error_analysis, 1, 7) == "statnet") {
                        # nodefactor in statnet appears to be not quite the same as R (Activity) in PNet, adjust by subtracting 0.5 from estimate (log-odds) for the statnet value
                        De$Estimate <- De$Estimate - 0.5
                    }

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
                    ## print(num_seedsets)

                    cat(network_N, attribute_descr, error_analysis, fixeddensity, 
                        gsub('_', ' ', effect), sub('_', ' ', zero_effect),
                        bias, rmse, false_positive_perc,
                        mean(De$StdErr), sd(De$Estimate), mean(De$convergedRuns),
                        fpp_lower, fpp_upper, num_seedsets,
                        length(De$Estimate), totalRuns, perc_in_ci,
                        sep=' & ')
                    cat('\\\\\n')
		}


}

