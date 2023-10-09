#!/usr/bin/env Rscript
##
## File:    runDevilSienaModel10.R
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
##   model10.html
##   model10.tex
##   model10.txt
##   model10_siena_gof_degree.eps
##   model10_siena_gof_geodesic.eps
##   model10_siena_gof_behavior.eps
##

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

model10data <- sienaDataCreate(contact, sex, Wound_status, Tumour_dep, Mating_season)

print01Report(data = model10data, modelname="model10")

model10effects<-getEffects(model10data)
model10effects <- includeEffects(model10effects, RateX, type="rate", interaction1="sex")
model10effects <- includeEffects(model10effects, RateX, type="rate", interaction1="Tumour_dep")
model10effects <- includeEffects(model10effects, RateX, type="rate", interaction1="Wound_status")
## Note using special effects for non-directed networks (RSiena manual s. 12.1.2)
model10effects <- includeEffects(model10effects, egoPlusAltX, interaction1="sex") # egoPlusAltSqX on sex is too correlated with density so dropped
model10effects <- includeEffects(model10effects, egoPlusAltX, egoPlusAltSqX,interaction1="Wound_status")
model10effects <- includeEffects(model10effects, egoPlusAltX, egoPlusAltSqX,interaction1="Tumour_dep")
## Model 04 adds degPlus and transTriads to Model 03
## (Model 03 has bad gof on geodesic distance and egree)
model10effects <- includeEffects(model10effects, degPlus)
model10effects <- includeEffects(model10effects, transTriads)

## Model 10 adds covariate for mating / non-mating season
## to test effect on rate (this is N.A. - so removed)
## and on tie formation and "behavior" outcome (tumour grad).
## Note that (obviously) the season in each
## time period is the same for all devils.
## Note that when an actor covariate is constant within waves (like
## Mating_season), then only the ego effect of rhte actor covariate is
## available (see RSiena manual (2018) s. 4.1.4 (p. 27))
#model10effects <- includeEffects(model10effects, RateX, type="rate", interaction1="Mating_season")
model10effects <- includeEffects(model10effects, egoX, interaction1="Mating_season")
## does not converge (not pos def covariancce matrix):
#model10effects <- includeEffects(model10effects, name = "Tumour_dep", effFrom, interaction1 = "Mating_season")


## The default modelType for undirected networks in sienaAlgorithm is
## being used here, which is 2 for "dictatorial forcing": one actor
## takes the initiative and unilaterlaly imposes that a tie is crated
## or dissolved (see RSiena manual and citations therein). This makes
## sense for this data, which is a contact network (from proximity
## logger data).
##
## Note also that Tumour_dep is always up; the number of tumours never
## decreases. RSiena detects this and estimates conditional on it by default.

model10alg <- sienaAlgorithmCreate(cond=TRUE, projname="model10")


## Estimate model
model10 <- siena07(model10alg, batch=TRUE, data=model10data, effects=model10effects, returnDeps=TRUE)

print(summary(model10))

## Output HTML and LaTeX tables
siena.table(model10, type='html', sig=TRUE)
siena.table(model10, type='tex', sig=TRUE)

## Goodness-of-fit
model10gof_behavior <- sienaGOF(model10, BehaviorDistribution, varName="Tumour_dep")
print(model10gof_behavior)
model10gof_degree <- sienaGOF(model10, OutdegreeDistribution, varName="contact")
print(model10gof_degree)
model10gof_geodesic <- sienaGOF(model10, GeodesicDistribution, varName="contact")
print(model10gof_geodesic)

## Don't seem to be able to do multiple plots like this with RSiene
## (unlike statnet) so have to do three separate plots inteaad
##par(mfrow=c(3,1))
postscript('model10_siena_gof_degree.eps')
plot(model10gof_degree)
dev.off()
postscript('model10_siena_gof_geodesic.eps')
plot(model10gof_geodesic)
dev.off()
postscript('model10_siena_gof_behavior.eps')
plot(model10gof_behavior)
dev.off()


