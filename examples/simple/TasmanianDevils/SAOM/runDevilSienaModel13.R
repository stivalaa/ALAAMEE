#!/usr/bin/env Rscript
##
## File:    runDevilSienaModel13.R
## Author:  Alex Stivala
## Created: October 2023
##
## Stochastic-actor oriented model (SAOM) estimation with RSiena for data from:
##
##   Hamilton, D. G., Jones, M. E., Cameron, E. Z., Kerlin, D. H.,
##   McCallum, H., Storfer, A., ... & Hamede, R. K. (2020). Infectious
##   disease and sickness behaviour: tumour progression affects
##   interaction patterns and social network structure in wild
##   Tasmanian devils. Proceedings of the Royal Society B, 287(1940),
##   20202454.
##
## using the replication data (in ../data/ directory) from dryad repository
## https://dx.doi.org/10.5061/dryad.xksn02vdp
##
##
## Output files in cwd (WARNING: overwrites):
##
##   model13.html
##   model13.tex
##   model13.txt
##   model13_siena_gof_degree.eps
##   model13_siena_gof_geodesic.eps
##   model13_siena_gof_behavior.eps
##

start_time <- Sys.time()
print(start_time)

library(RSiena)

sessionInfo()

source('load_data.R')
source('GeodesicDistribution.R')


contactData <- array(c(as.matrix(f1),as.matrix(f2),as.matrix(f3),as.matrix(f4),as.matrix(f5),as.matrix(f6),as.matrix(f7),as.matrix(f8),as.matrix(f9),as.matrix(f10),as.matrix(f11),as.matrix(f12)), dim = c(22, 22, 12))
contact <- sienaDependent(contactData)

sex <- coCovar(Sex$Sex)
Wound_status <- varCovar(as.matrix(Wounds[,2:13]))
## Number of tumours as dependent variable
Tumour_dep <- sienaDependent( as.matrix(Tumour[2:13]), type="behavior")

## Model 10 adds covariate for mating / non-mating season
## Note that (obviously) the season in each
## time period is the same for all devils.
Mating_season <- varCovar( as.matrix(Season[,2:13]) )

model13data <- sienaDataCreate(contact, sex, Wound_status, Tumour_dep, Mating_season)

print01Report(data = model13data, modelname="model13")

model13effects<-getEffects(model13data)
model13effects <- includeEffects(model13effects, RateX, type="rate", interaction1="sex")
model13effects <- includeEffects(model13effects, RateX, type="rate", interaction1="Tumour_dep")
model13effects <- includeEffects(model13effects, RateX, type="rate", interaction1="Wound_status")
## Note using special effects for non-directed networks (RSiena manual s. 12.1.2)
model13effects <- includeEffects(model13effects, egoPlusAltX, interaction1="sex") ## egoPlusAltSqX for sex is too correlated with degree(density) so dropped
model13effects <- includeEffects(model13effects, egoPlusAltX, egoPlusAltSqX,interaction1="Wound_status")
model13effects <- includeEffects(model13effects, egoPlusAltX, egoPlusAltSqX,interaction1="Tumour_dep")
## Model 04 adds degPlus and transTriads to Model 03
## (Model 03 has bad gof on geodesic distance and egree)
model13effects <- includeEffects(model13effects, transTriads)

## For Model 13, try inPop and outAct separately insteda of degPlus
#model13effects <- includeEffects(model13effects, degPlus)
##model13effects <- includeEffects(model13effects, inPop, outAct)
## But (predictably enough) this does not work as inPop and outAct
## are colinear so get not postivie definite covariance matrix
## So instead try outActSqrt
#model13effects <- includeEffects(model13effects, outActSqrt)
## didn't change anything compared to degPlus (Model 12), so try this instead:
##model13effects <- includeEffects(model13effects, outAct, outActSqrt)
## seems better gof, but overall max conv. ratio was 2.53 so try this instead:
### Does not converge:
#model13effects <- includeEffects(model13effects, outAct, outSqInv)
## So try this instead:
#model13effects <- includeEffects(model13effects,  outSqInv)
# but it also does not converge

model13effects <- includeEffects(model13effects, outAct, outActSqrt)


## Model 10 adds covariate for mating / non-mating season
## to test effect on rate (this is N.A. - so removed)
## and on tie formation and "behavior" outcome (tumour grad).
## Note that (obviously) the season in each
## time period is the same for all devils.
## Note that when an actor covariate is constant within waves (like
## Mating_season), then only the ego effect of rhte actor covariate is
## available (see RSiena manual (2018) s. 4.1.4 (p. 27))
#model13effects <- includeEffects(model13effects, RateX, type="rate", interaction1="Mating_season")
model13effects <- includeEffects(model13effects, egoX, interaction1="Mating_season")
## does not converge (not pos def covariancce matrix):
#model13effects <- includeEffects(model13effects, name = "Tumour_dep", effFrom, interaction1 = "Mating_season")

## Model 11 adds monadic covariate effects for Tumour grade "behaviour" variable
model13effects <- includeEffects(model13effects, name = "Tumour_dep", effFrom, interaction1 = "sex")
model13effects <- includeEffects(model13effects, name = "Tumour_dep", effFrom, interaction1 = "Wound_status")

## Model 12 adds effect for alter new wound counts
model13effects <- includeEffects(model13effects, name = "Tumour_dep", totXAlt, interaction1 = "Wound_status", interaction2 = "contact")

## Model 13 adds isolate structural effect to try to fix bad gof
## of Model 12 on degree distribution where degree is 0
#model13effects <- includeEffects(model13effects, isolateNet)
## Turns out get estiamte N.A. for some reason, so no change,
## try degree assortativiy instead (note outInAss is the appropriate
## one for undirected networks, see RSieana manual section 12.1.2)
#model13effects <- includeEffects(model13effects, outInAss)
## outInAss does not inprove degree gof and has worse convergence
## (overal max 0.99 on first try)


## The default modelType for undirected networks in sienaAlgorithm is
## being used here, which is 2 for "dictatorial forcing": one actor
## takes the initiative and unilaterlaly imposes that a tie is crated
## or dissolved (see RSiena manual and citations therein). This makes
## sense for this data, which is a contact network (from proximity
## logger data).
##
## Note also that Tumour_dep is always up; the number of tumours never
## decreases. RSiena detects this and estimates conditional on it by default.

model13alg <- sienaAlgorithmCreate(cond=TRUE, projname="model13")


## Estimate model
model13 <- siena07(model13alg, batch=TRUE, data=model13data, effects=model13effects, returnDeps=TRUE)
## Does not converge if try to continue, get error:
##
#Error in x$FRAN(zdummy, xsmall, fromFiniteDiff = TRUE) :
#  Unlikely to terminate this epoch:  more than 1000000 steps
#Calls: siena07 ... doPhase1or3Iterations -> FiniteDifferences -> <Anonymous>
#Execution halted
#
model13 <- siena07(model13alg, batch=TRUE, data=model13data, effects=model13effects, returnDeps=TRUE, prevAns = model13)

print(summary(model13))

## Output HTML and LaTeX tables
siena.table(model13, type='html', sig=TRUE)
siena.table(model13, type='tex', sig=TRUE)

## Goodness-of-fit
model13gof_behavior <- sienaGOF(model13, BehaviorDistribution, varName="Tumour_dep")
print(model13gof_behavior)
model13gof_degree <- sienaGOF(model13, OutdegreeDistribution, varName="contact")
print(model13gof_degree)
model13gof_geodesic <- sienaGOF(model13, GeodesicDistribution, varName="contact")
print(model13gof_geodesic)

## Don't seem to be able to do multiple plots like this with RSiene
## (unlike statnet) so have to do three separate plots inteaad
##par(mfrow=c(3,1))
postscript('model13_siena_gof_degree.eps')
plot(model13gof_degree)
dev.off()
postscript('model13_siena_gof_geodesic.eps')
plot(model13gof_geodesic)
dev.off()
postscript('model13_siena_gof_behavior.eps')
plot(model13gof_behavior)
dev.off()

end_time <- Sys.time()
print(end_time)
print(end_time - start_time)
