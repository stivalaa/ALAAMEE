#!/usr/bin/env Rscript
##
## File:    runDevilSienaModel04.R
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
##   model04.html
##   model04.tex
##   model04.txt
##   model04_siena_gof_degree.eps
##   model04_siena_gof_geodesic.eps
##   model04_siena_gof_behavior.eps
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

model04data <- sienaDataCreate(contact, sex, Wound_status, Tumour_dep)

print01Report(data = model04data, modelname="model04")

model04effects<-getEffects(model04data)
model04effects <- includeEffects(model04effects, RateX, type="rate", interaction1="sex")
model04effects <- includeEffects(model04effects, RateX, type="rate", interaction1="Tumour_dep")
model04effects <- includeEffects(model04effects, RateX, type="rate", interaction1="Wound_status")
## Note using special effects for non-directed networks (RSiena manual s. 12.1.2)
model04effects <- includeEffects(model04effects, egoPlusAltX, interaction1="sex") # egoPlusAltSqX is too correlated with density so dropped
model04effects <- includeEffects(model04effects, egoPlusAltX, egoPlusAltSqX,interaction1="Wound_status")
model04effects <- includeEffects(model04effects, egoPlusAltX, egoPlusAltSqX,interaction1="Tumour_dep")
## Model 04 adds degPlus and transTriads to Model 03
## (Model 03 has bad gof on geodesic distance and egree)
model04effects <- includeEffects(model04effects, degPlus)
model04effects <- includeEffects(model04effects, transTriads)


## The default modelType for undirected networks in sienaAlgorithm is
## being used here, which is 2 for "dictatorial forcing": one actor
## takes the initiative and unilaterlaly imposes that a tie is crated
## or dissolved (see RSiena manual and citations therein). This makes
## sense for this data, which is a contact network (from proximity
## logger data).
##
## Note also that Tumour_dep is always up; the number of tumours never
## decreases. RSiena detects this and estimates conditional on it by default.

model04alg <- sienaAlgorithmCreate(cond=TRUE, projname="model04")


## Estimate model
model04 <- siena07(model04alg, batch=TRUE, data=model04data, effects=model04effects, returnDeps=TRUE)

print(summary(model04))

## Output HTML and LaTeX tables
siena.table(model04, type='html', sig=TRUE)
siena.table(model04, type='tex', sig=TRUE)

## Goodness-of-fit
model04gof_behavior <- sienaGOF(model04, BehaviorDistribution, varName="Tumour_dep")
print(model04gof_behavior)
model04gof_degree <- sienaGOF(model04, OutdegreeDistribution, varName="contact")
print(model04gof_degree)
model04gof_geodesic <- sienaGOF(model04, GeodesicDistribution, varName="contact")
print(model04gof_geodesic)

## Don't seem to be able to do multiple plots like this with RSiene
## (unlike statnet) so have to do three separate plots inteaad
##par(mfrow=c(3,1))
postscript('model04_siena_gof_degree.eps')
plot(model04gof_degree)
dev.off()
postscript('model04_siena_gof_geodesic.eps')
plot(model04gof_geodesic)
dev.off()
postscript('model04_siena_gof_behavior.eps')
plot(model04gof_behavior)
dev.off()

end_time <- Sys.time()
print(end_time)
print(end_time - start_time)
