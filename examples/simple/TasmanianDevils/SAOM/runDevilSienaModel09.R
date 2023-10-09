#!/usr/bin/env Rscript
##
## File:    runDevilSienaModel09.R
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
##   model09.html
##   model09.tex
##   model09.txt
##   model09_siena_gof_degree.eps
##   model09_siena_gof_geodesic.eps
##   model09_siena_gof_behavior.eps
##
##
## This model uses number of wounds as the dependent variable, like the
## network autocorrelation models in:
##
##   Hamilton, D. G., Jones, M. E., Cameron, E. Z., McCallum, H.,
##   Storfer, A., Hohenlohe, P. A., & Hamede, R. K. (2019). Rate of
##   intersexual interactions affects injury likelihood in Tasmanian
##   devil contact networks. Behavioral Ecology, 30(4), 1087-1095.
##
## Note that in the earlier models, number of tumours was used as the
## dependent variable, but only rate parameters were included, as the
## model would not converge if for example avAlt is included wiht
## e.g. includeEffects(model05effects, name = "Tumour_dep", avAlt,
## interaction1="contact")

##
## This model does not converge, after about 45 minutes
## (Model 03 and Model 04 both converge in about 5 minutes)
##


library(RSiena)

sessionInfo()

source('load_data.R')
source('GeodesicDistribution.R')


contactData <- array(c(as.matrix(f1),as.matrix(f2),as.matrix(f3),as.matrix(f4),as.matrix(f5),as.matrix(f6),as.matrix(f7),as.matrix(f8),as.matrix(f9),as.matrix(f10),as.matrix(f11),as.matrix(f12)), dim = c(22, 22, 12))
contact <- sienaDependent(contactData)

sex <- coCovar(Sex$Sex)
Tumour_status <- varCovar(as.matrix(Tumour[,2:13]))
## Number of wounds as dependent variable
Wound_dep <- sienaDependent( as.matrix(Wounds[2:13]), type="behavior")

model09data <- sienaDataCreate(contact, sex, Tumour_status, Wound_dep)

print01Report(data = model09data, modelname="model09")

model09effects<-getEffects(model09data)
model09effects <- includeEffects(model09effects, RateX, type="rate", interaction1="sex")
model09effects <- includeEffects(model09effects, RateX, type="rate", interaction1="Tumour_status")
model09effects <- includeEffects(model09effects, RateX, type="rate", interaction1="Wound_dep")
model09effects <- includeEffects(model09effects, altX, egoXaltX,interaction1="sex")
model09effects <- includeEffects(model09effects, altX, egoXaltX,interaction1="Wound_dep")
model09effects <- includeEffects(model09effects, altX, egoXaltX,interaction1="Tumour_status")
model09effects <- includeEffects(model09effects, degPlus)
model09effects <- includeEffects(model09effects, transTriads)

## Add "behavior" effect for wound count (effect of contact network on wound count)
model09effects <- includeEffects(model09effects, name = "Wound_dep", avAlt, interaction1="contact")


## The default modelType for undirected networks in sienaAlgorithm is
## being used here, which is 2 for "dictatorial forcing": one actor
## takes the initiative and unilaterlaly imposes that a tie is crated
## or dissolved (see RSiena manual and citations therein). This makes
## sense for this data, which is a contact network (from proximity
## logger data).

model09alg <- sienaAlgorithmCreate(cond=TRUE, projname="model09")


## Estimate model
model09 <- siena07(model09alg, batch=TRUE, data=model09data, effects=model09effects, returnDeps=TRUE)

print(summary(model09))

## Output HTML and LaTeX tables
siena.table(model09, type='html', sig=TRUE)
siena.table(model09, type='tex', sig=TRUE)

## Goodness-of-fit
model09gof_behavior <- sienaGOF(model09, BehaviorDistribution, varName="Wound_dep")
print(model09gof_behavior)
model09gof_degree <- sienaGOF(model09, OutdegreeDistribution, varName="contact")
print(model09gof_degree)
model09gof_geodesic <- sienaGOF(model09, GeodesicDistribution, varName="contact")
print(model09gof_geodesic)

## Don't seem to be able to do multiple plots like this with RSiene
## (unlike statnet) so have to do three separate plots inteaad
##par(mfrow=c(3,1))
postscript('model09_siena_gof_degree.eps')
plot(model09gof_degree)
dev.off()
postscript('model09_siena_gof_geodesic.eps')
plot(model09gof_geodesic)
dev.off()
postscript('model09_siena_gof_behavior.eps')
plot(model09gof_behavior)
dev.off()


