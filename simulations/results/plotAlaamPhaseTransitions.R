#!/usr/bin/Rscript
##
## File:    ploAlaamPhaseTransitions.R
## Author:  Alex Stivala
## Created: July 2023
##
## Produce plots showing phase transition (near-degeneracy) behaviour in
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
## Reads data from output of ALAAM runs in ../AlaamSimulations/
## Outputs EPS files in cwd (WARNING: overwrites).
##
##

source('plot_mean_and_variance.R')

###
### main
###

dat <- read.table('../AlaamSimulations/project90Simulations/stats_sim_project90.txt', header = TRUE)
plot_mean_and_variance("Contagion", "Density", "project90")
plot_mean_and_variance("Contagion", "Contagion", "project90")


dat <- read.table("../AlaamSimulations/project90noAttrSimulations/Activity/stats_sim_project90noattr.txt", header = TRUE)
plot_mean_and_variance("Activity", "Density", "project90noAttr")
plot_mean_and_variance("Activity", "Activity", "project90noAttr")

dat <- read.table("../AlaamSimulations/project90noAttrSimulations/Contagion/stats_sim_project90noattr.txt", header = TRUE)
plot_mean_and_variance("Contagion", "Density", "project90noAttr")
plot_mean_and_variance("Contagion", "Contagion", "project90noAttr")

dat <- read.table("../AlaamSimulations/project90noAttrSimulations/TwoStar/stats_sim_project90noattr.txt", header = TRUE)
plot_mean_and_variance("Two.Star", "Density", "project90noAttr")
plot_mean_and_variance("Two.Star", "Two.Star", "project90noAttr")



obs <- read.table('../AlaamSimulations/deezerEuropeSimulations/observed/obs_stats_sim_deezer_europe.txt', header = TRUE)
dat <- read.table("../AlaamSimulations/deezerEuropeSimulations/Activity/stats_sim_deezer.txt", header = TRUE)
plot_mean_and_variance("Activity", "Density", "deezer")
plot_mean_and_variance("Activity", "Activity", "deezer", obs)
plot_mean_and_variance("Activity", "Contagion", "deezer")

dat <- read.table("../AlaamSimulations/deezerEuropeSimulations/Contagion/stats_sim_deezer.txt", header = TRUE)
plot_mean_and_variance("Contagion", "Density", "deezer")
plot_mean_and_variance("Contagion", "Contagion", "deezer", obs)

dat <- read.table("../AlaamSimulations/deezerEuropeSimulations/TwoStar/stats_sim_deezer.txt", header = TRUE)
plot_mean_and_variance("Two.Star", "Density", "deezer")
plot_mean_and_variance("Two.Star", "Two.Star", "deezer", obs)


obs <- read.table('../AlaamSimulations/higgsTwitterSimulations/observed/obs_stats_sim_higgs_europe_outcome_reply.txt', header = TRUE)
dat <- read.table("../AlaamSimulations/higgsTwitterSimulations/Contagion/stats_sim_higgs.txt", header = TRUE)
plot_mean_and_variance("Contagion", "Density", "higgs")
plot_mean_and_variance("Contagion", "Contagion", "higgs", obs)

dat <- read.table("../AlaamSimulations/higgsTwitterSimulations/Sender/stats_sim_higgs.txt", header = TRUE)
plot_mean_and_variance("Sender", "Density", "higgs")
plot_mean_and_variance("Sender", "Contagion", "higgs")
plot_mean_and_variance("Sender", "Sender", "higgs", obs)

dat <- read.table("../AlaamSimulations/higgsTwitterSimulations/Receiver/stats_sim_higgs.txt", header = TRUE)
plot_mean_and_variance("Receiver", "Density", "higgs")
plot_mean_and_variance("Receiver", "Contagion", "higgs")
plot_mean_and_variance("Receiver", "Receiver", "higgs", obs)


obs <- read.table('../AlaamSimulations/GitHubSimulations/observed/obs_stats_sim_github_europe.txt', header = TRUE)
dat <- read.table("../AlaamSimulations/GitHubSimulations/Activity/stats_sim_github.txt", header = TRUE)
plot_mean_and_variance("Activity", "Density", "github")
plot_mean_and_variance("Activity", "Activity", "github", obs)
plot_mean_and_variance("Activity", "Contagion", "github")
print(obs)#XXX
plot_mean_and_variance("Activity", "meanDegree1", "github", obs)
plot_mean_and_variance("Activity", "varDegree1", "github", obs)


dat <- read.table("../AlaamSimulations/GitHubSimulations/Contagion/stats_sim_github.txt", header = TRUE)
plot_mean_and_variance("Contagion", "Density", "github")
plot_mean_and_variance("Contagion", "Contagion", "github", obs)


obs <- read.table('../AlaamSimulations/pokec/observed/obs_stats_sim_pokec_europe.txt', header = TRUE)
dat <- read.table("../AlaamSimulations/pokec/Activity/stats_sim_pokec.txt", header = TRUE)
plot_mean_and_variance("Activity", "Density", "pokec")
plot_mean_and_variance("Activity", "Activity", "pokec", obs)
plot_mean_and_variance("Activity", "Contagion", "pokec")
plot_mean_and_variance("Activity", "meanDegree1", "pokec", obs)
plot_mean_and_variance("Activity", "varDegree1", "pokec", obs)

dat <- read.table("../AlaamSimulations/pokec/Contagion/stats_sim_pokec.txt", header = TRUE)
plot_mean_and_variance("Contagion", "Density", "pokec")
plot_mean_and_variance("Contagion", "Contagion", "pokec", obs)


dat <- read.table("../AlaamSimulations/latticeSimulations/Activity/stats_sim_lattice.txt", header = TRUE)
plot_mean_and_variance("Activity", "Density", "lattice")
plot_mean_and_variance("Activity", "Activity", "lattice")
plot_mean_and_variance("Activity", "Contagion", "lattice")

dat <- read.table("../AlaamSimulations/latticeSimulations/Contagion/stats_sim_lattice.txt", header = TRUE)
plot_mean_and_variance("Contagion", "Density", "lattice")
plot_mean_and_variance("Contagion", "Contagion", "lattice")



obs <- read.table('../AlaamSimulations/HighSchoolFriendship/observed/obs_stats_sim_highschool.txt', header = TRUE)
dat <- read.table("../AlaamSimulations/HighSchoolFriendship/Sender/stats_sim_highschool.txt", header = TRUE)
plot_mean_and_variance("Sender", "Density", "highschool")
plot_mean_and_variance("Sender", "Contagion", "highschool")
plot_mean_and_variance("Sender", "Sender", "highschool", obs)
plot_mean_and_variance("Sender", "meanInDegree1", "highschool", obs)
plot_mean_and_variance("Sender", "varInDegree1", "highschool", obs)
plot_mean_and_variance("Sender", "meanOutDegree1", "highschool", obs)
plot_mean_and_variance("Sender", "varOutDegree1", "highschool", obs)

dat <- read.table("../AlaamSimulations/HighSchoolFriendship/Receiver/stats_sim_highschool.txt", header = TRUE)
plot_mean_and_variance("Receiver", "Density", "highschool")
plot_mean_and_variance("Receiver", "Contagion", "highschool")
plot_mean_and_variance("Receiver", "Receiver", "highschool", obs)
plot_mean_and_variance("Receiver", "meanInDegree1", "highschool", obs)
plot_mean_and_variance("Receiver", "varInDegree1", "highschool", obs)
plot_mean_and_variance("Receiver", "meanOutDegree1", "highschool", obs)
plot_mean_and_variance("Receiver", "varOutDegree1", "highschool", obs)
