#!/usr/bin/Rscript
##
## File:    ploAlaamPhaseTransitionsGW.R
## Author:  Alex Stivala
## Created: August 2023
##
## Produce plots showing phase transition (near-degeneracy), or lack
## thereof, behaviour when using geometrically weighted statistics in
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
##
## Reads data from output of ALAAM runs in 
## ../AlaamSimulations/geometrically_weighted/
## Outputs EPS files in cwd (WARNING: overwrites).
##
##

source('plot_mean_and_variance.R')

###
### main
###

dat <- read.table('../AlaamSimulations/geometrically_weighted/project90Simulations/stats_sim_project90.txt', header = TRUE)
plot_mean_and_variance("GWContagion", "Density", "project90")
plot_mean_and_variance("GWContagion", "Contagion", "project90")
plot_mean_and_variance("GWContagion", "GWContagion", "project90")


dat <- read.table("../AlaamSimulations/geometrically_weighted/project90noAttrSimulations/GWActivity/stats_sim_project90noattr.txt", header = TRUE)
plot_mean_and_variance("GWActivity", "Density", "project90noAttr")
plot_mean_and_variance("GWActivity", "Activity", "project90noAttr")
plot_mean_and_variance("GWActivity", "Contagion", "project90noAttr")
plot_mean_and_variance("GWActivity", "GWActivity", "project90noAttr")


obs <- read.table('../AlaamSimulations/geometrically_weighted/deezerEuropeSimulations/observed/obs_stats_sim_deezer_europe.txt', header = TRUE)
## Remove alpha value suffix from GW paramters in observed data so they match
## those in the simulated data (which was done without these suffixes)
## e.g. "GWActivity.0.6931471805599453" -> "GWActivity"
colnames(obs) <- gsub("[.][0-9.]*", "", colnames(obs))
dat <- read.table("../AlaamSimulations/geometrically_weighted/deezerEuropeSimulations/GWActivity/stats_sim_deezer.txt", header = TRUE)
plot_mean_and_variance("GWActivity", "Density", "deezer")
plot_mean_and_variance("GWActivity", "Activity", "deezer")
plot_mean_and_variance("GWActivity", "Contagion", "deezer")
plot_mean_and_variance("GWActivity", "GWActivity", "deezer", obs)

dat <- read.table("../AlaamSimulations/geometrically_weighted/deezerEuropeSimulations/GWContagion/stats_sim_deezer.txt", header = TRUE)
plot_mean_and_variance("GWContagion", "Density", "deezer")
plot_mean_and_variance("GWContagion", "Contagion", "deezer")
plot_mean_and_variance("GWContagion", "GWContagion", "deezer", obs)


obs <- read.table('../AlaamSimulations/geometrically_weighted/higgsTwitterSimulations/observed/obs_stats_sim_higgs_europe_outcome_reply.txt', header = TRUE)
## Remove alpha value suffix from GW paramters in observed data so they match
## those in the simulated data (which was done without these suffixes)
## e.g. "GWActivity.0.6931471805599453" -> "GWActivity"
colnames(obs) <- gsub("[.][0-9.]*", "", colnames(obs))
dat <- read.table("../AlaamSimulations/geometrically_weighted/deezerEuropeSimulations/GWActivity/stats_sim_deezer.txt", header = TRUE)
dat <- read.table("../AlaamSimulations/geometrically_weighted/higgsTwitterSimulations/GWReceiver/stats_sim_higgs.txt", header = TRUE)
plot_mean_and_variance("GWReceiver", "Density", "higgs")
plot_mean_and_variance("GWReceiver", "Contagion", "higgs")
plot_mean_and_variance("GWReceiver", "GWReceiver", "higgs", obs)
plot_mean_and_variance("GWReceiver", "Receiver", "higgs")

dat <- read.table("../AlaamSimulations/geometrically_weighted/higgsTwitterSimulations/GWSender/stats_sim_higgs.txt", header = TRUE)
plot_mean_and_variance("GWSender", "Density", "higgs")
plot_mean_and_variance("GWSender", "Contagion", "higgs")
plot_mean_and_variance("GWSender", "GWSender", "higgs", obs)
plot_mean_and_variance("GWSender", "Sender", "higgs")

dat <- read.table("../AlaamSimulations/geometrically_weighted/higgsTwitterSimulations/GWContagion/stats_sim_higgs.txt", header = TRUE)
plot_mean_and_variance("GWContagion", "Density", "higgs")
plot_mean_and_variance("GWContagion", "Contagion", "higgs")
plot_mean_and_variance("GWContagion", "GWContagion", "higgs", obs)



obs <- read.table('../AlaamSimulations/geometrically_weighted/GitHubSimulations/observed/obs_stats_sim_github_europe.txt', header = TRUE)
## Remove alpha value suffix from GW paramters in observed data so they match
## those in the simulated data (which was done without these suffixes)
## e.g. "GWActivity.0.6931471805599453" -> "GWActivity"
colnames(obs) <- gsub("[.][0-9.]*", "", colnames(obs))
dat <- read.table("../AlaamSimulations/geometrically_weighted/GitHubSimulations/GWActivity/stats_sim_github.txt", header = TRUE)
plot_mean_and_variance("GWActivity", "Density", "github")
plot_mean_and_variance("GWActivity", "Activity", "github")
plot_mean_and_variance("GWActivity", "Contagion", "github")
plot_mean_and_variance("GWActivity", "GWActivity", "github", obs)

dat <- read.table("../AlaamSimulations/geometrically_weighted/GitHubSimulations/GWContagion/stats_sim_github.txt", header = TRUE)
plot_mean_and_variance("GWContagion", "Density", "github")
plot_mean_and_variance("GWContagion", "Contagion", "github")
plot_mean_and_variance("GWContagion", "GWContagion", "github", obs)

dat <- read.table("../AlaamSimulations/geometrically_weighted/GitHubSimulations/GWActivity_gwparams/stats_sim_github.txt", header = TRUE)
plot_mean_and_variance("GWActivity", "Density", "github_gwparams")
plot_mean_and_variance("GWActivity", "Activity", "github_gwparams")
plot_mean_and_variance("GWActivity", "Contagion", "github_gwparams")
plot_mean_and_variance("GWActivity", "GWActivity", "github_gwparams", obs)
plot_mean_and_variance("GWActivity", "meanDegree1", "github_gwparams", obs)
plot_mean_and_variance("GWActivity", "varDegree1", "github_gwparams", obs)

dat <- read.table("../AlaamSimulations/geometrically_weighted/GitHubSimulations/GWContagion_gwparams/stats_sim_github.txt", header = TRUE)
plot_mean_and_variance("GWContagion", "Density", "github_gwparams")
plot_mean_and_variance("GWContagion", "Contagion", "github_gwparams")
plot_mean_and_variance("GWContagion", "GWContagion", "github_gwparams", obs)

dat <- read.table("../AlaamSimulations/geometrically_weighted/GitHubSimulations/Contagion_gwparams/stats_sim_github.txt", header= TRUE)
plot_mean_and_variance("Contagion", "Density", "github_gwparams")
plot_mean_and_variance("Contagion", "Contagion", "github_gwparams", obs)
plot_mean_and_variance("Contagion", "meanDegree1", "github_gwparams", obs)
plot_mean_and_variance("Contagion", "varDegree1", "github_gwparams", obs)



obs <- read.table('../AlaamSimulations/geometrically_weighted/pokec/observed/obs_stats_sim_pokec_europe.txt', header = TRUE)
## Remove alpha value suffix from GW paramters in observed data so they match
## those in the simulated data (which was done without these suffixes)
## e.g. "GWActivity.0.6931471805599453" -> "GWActivity"
colnames(obs) <- gsub("[.][0-9.]*", "", colnames(obs))
dat <- read.table("../AlaamSimulations/geometrically_weighted/pokec/GWActivity/stats_sim_pokec.txt", header = TRUE)
plot_mean_and_variance("GWActivity", "Density", "pokec")
plot_mean_and_variance("GWActivity", "Activity", "pokec")
plot_mean_and_variance("GWActivity", "Contagion", "pokec")
plot_mean_and_variance("GWActivity", "GWActivity", "pokec", obs)
plot_mean_and_variance("GWActivity", "meanDegree1", "pokec", obs)
plot_mean_and_variance("GWActivity", "varDegree1", "pokec", obs)

dat <- read.table("../AlaamSimulations/geometrically_weighted/pokec/GWContagion/stats_sim_pokec.txt", header = TRUE)
plot_mean_and_variance("GWContagion", "Density", "pokec")
plot_mean_and_variance("GWContagion", "Contagion", "pokec")
plot_mean_and_variance("GWContagion", "GWContagion", "pokec", obs)

dat <- read.table("../AlaamSimulations/geometrically_weighted/pokec/Contagion_gwparams/stats_sim_pokec.txt", header = TRUE)
plot_mean_and_variance("Contagion", "Density", "pokec_gwparams")
plot_mean_and_variance("Contagion", "Contagion", "pokec_gwparams", obs)

dat <- read.table("../AlaamSimulations/geometrically_weighted/pokec/GWActivity_gwparams/stats_sim_pokec.txt", header = TRUE)
plot_mean_and_variance("GWActivity", "Density", "pokec_gwparams")
plot_mean_and_variance("GWActivity", "Contagion", "pokec_gwparams", obs)
plot_mean_and_variance("GWActivity", "GWActivity", "pokec_gwparams", obs)
plot_mean_and_variance("GWActivity", "meanDegree1", "pokec_gwparams", obs)
plot_mean_and_variance("GWActivity", "varDegree1", "pokec_gwparams", obs)



dat <- read.table("../AlaamSimulations/geometrically_weighted/latticeSimulations/GWActivity/stats_sim_lattice.txt", header = TRUE)
plot_mean_and_variance("GWActivity", "Density", "lattice")
plot_mean_and_variance("GWActivity", "Activity", "lattice")
plot_mean_and_variance("GWActivity", "Contagion", "lattice")
plot_mean_and_variance("GWActivity", "GWActivity", "lattice")

dat <- read.table("../AlaamSimulations/geometrically_weighted/latticeSimulations/GWContagion/stats_sim_lattice.txt", header = TRUE)
plot_mean_and_variance("GWContagion", "Density", "lattice")
plot_mean_and_variance("GWContagion", "Contagion", "lattice")
plot_mean_and_variance("GWContagion", "GWContagion", "lattice")



obs <- read.table('../AlaamSimulations/geometrically_weighted/HighSchoolFriendship/observed/obs_stats_sim_highschool.txt', header = TRUE)
## Remove alpha value suffix from GW paramters in observed data so they match
## those in the simulated data (which was done without these suffixes)
## e.g. "GWActivity.0.6931471805599453" -> "GWActivity"
colnames(obs) <- gsub("[.][0-9.]*", "", colnames(obs))
dat <- read.table("../AlaamSimulations/geometrically_weighted/HighSchoolFriendship/GWSender/stats_sim_highschool.txt", header = TRUE)
plot_mean_and_variance("GWSender", "Density", "highschool")
plot_mean_and_variance("GWSender", "Contagion", "highschool")
plot_mean_and_variance("GWSender", "Sender", "highschool", obs)
plot_mean_and_variance("GWSender", "GWSender", "highschool", obs)
plot_mean_and_variance("GWSender", "meanInDegree1", "highschool", obs)
plot_mean_and_variance("GWSender", "varInDegree1", "highschool", obs)
plot_mean_and_variance("GWSender", "meanOutDegree1", "highschool", obs)
plot_mean_and_variance("GWSender", "varOutDegree1", "highschool", obs)

dat <- read.table("../AlaamSimulations/geometrically_weighted/HighSchoolFriendship/GWReceiver/stats_sim_highschool.txt", header = TRUE)
plot_mean_and_variance("GWReceiver", "Density", "highschool")
plot_mean_and_variance("GWReceiver", "Contagion", "highschool")
plot_mean_and_variance("GWReceiver", "GWReceiver", "highschool", obs)
plot_mean_and_variance("GWReceiver", "Receiver", "highschool", obs)
plot_mean_and_variance("GWReceiver", "meanInDegree1", "highschool", obs)
plot_mean_and_variance("GWReceiver", "varInDegree1", "highschool", obs)
plot_mean_and_variance("GWReceiver", "meanOutDegree1", "highschool", obs)
plot_mean_and_variance("GWReceiver", "varOutDegree1", "highschool", obs)
