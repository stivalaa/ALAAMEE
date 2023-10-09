#####TERGM code for Tasmanian devil DFTD networks#####

#load packages
## xergm no longer available, now btergm instead
require(btergm)
library(network) #also need this

## print information about platform, packages, etc.
sessionInfo()

#read in matrices

f1<-read.csv("f1.csv")
names<-f1[,1]
f1<-sign(f1[,2:ncol(f1)])
rownames(f1)<-colnames(f1)<-names

f2<-read.csv("f2.csv")
names<-f2[,1]
f2<-sign(f2[,2:ncol(f2)])
rownames(f2)<-colnames(f2)<-names

f3<-read.csv("f3.csv")
names<-f3[,1]
f3<-sign(f3[,2:ncol(f3)])
rownames(f3)<-colnames(f3)<-names

f4<-read.csv("f4.csv")
names<-f4[,1]
f4<-sign(f4[,2:ncol(f4)])
rownames(f4)<-colnames(f4)<-names

f5<-read.csv("f5.csv")
names<-f5[,1]
f5<-sign(f5[,2:ncol(f5)])
rownames(f5)<-colnames(f5)<-names

f6<-read.csv("f6.csv")
names<-f6[,1]
f6<-sign(f6[,2:ncol(f6)])
rownames(f6)<-colnames(f6)<-names

f7<-read.csv("f7.csv")
names<-f7[,1]
f7<-sign(f7[,2:ncol(f7)])
rownames(f7)<-colnames(f7)<-names

f8<-read.csv("f8.csv")
names<-f8[,1]
f8<-sign(f8[,2:ncol(f8)])
rownames(f8)<-colnames(f8)<-names

f9<-read.csv("f9.csv")
names<-f9[,1]
f9<-sign(f9[,2:ncol(f9)])
rownames(f9)<-colnames(f9)<-names

f10<-read.csv("f10.csv")
names<-f10[,1]
f10<-sign(f10[,2:ncol(f10)])
rownames(f10)<-colnames(f10)<-names

f11<-read.csv("f11.csv")
names<-f11[,1]
f11<-sign(f11[,2:ncol(f11)])
rownames(f11)<-colnames(f11)<-names

f12<-read.csv("f12.csv")
names<-f12[,1]
f12<-sign(f12[,2:ncol(f12)])
rownames(f12)<-colnames(f12)<-names



#-------------------------------------------------------------

#read in DFTD status
DFTD<-read.csv("DFTDstatus.csv")
#and save to have separate info for each season
DFTDf1<-DFTD[,c(1,2)]
DFTDf2<-DFTD[,c(1,3)]
DFTDf3<-DFTD[,c(1,4)]
DFTDf4<-DFTD[,c(1,5)]
DFTDf5<-DFTD[,c(1,6)]
DFTDf6<-DFTD[,c(1,7)]
DFTDf7<-DFTD[,c(1,8)]
DFTDf8<-DFTD[,c(1,9)]
DFTDf9<-DFTD[,c(1,10)]
DFTDf10<-DFTD[,c(1,11)]
DFTDf11<-DFTD[,c(1,12)]
DFTDf12<-DFTD[,c(1,13)]


#read in Season (Mating season is a factor for everyone in f3 to f7)
Season<-read.csv("Season.csv")
#and save to have separate info for each season
Seasf1<-Season[,c(1,2)]
Seasf2<-Season[,c(1,3)]
Seasf3<-Season[,c(1,4)]
Seasf4<-Season[,c(1,5)]
Seasf5<-Season[,c(1,6)]
Seasf6<-Season[,c(1,7)]
Seasf7<-Season[,c(1,8)]
Seasf8<-Season[,c(1,9)]
Seasf9<-Season[,c(1,10)]
Seasf10<-Season[,c(1,11)]
Seasf11<-Season[,c(1,12)]
Seasf12<-Season[,c(1,13)]


#read in Tumour load
Tumour<-read.csv("TumourLoad_factor.csv")
#and save to have separate info for each season
TLdf1<-Tumour[,c(1,2)]
TLdf2<-Tumour[,c(1,3)]
TLdf3<-Tumour[,c(1,4)]
TLdf4<-Tumour[,c(1,5)]
TLdf5<-Tumour[,c(1,6)]
TLdf6<-Tumour[,c(1,7)]
TLdf7<-Tumour[,c(1,8)]
TLdf8<-Tumour[,c(1,9)]
TLdf9<-Tumour[,c(1,10)]
TLdf10<-Tumour[,c(1,11)]
TLdf11<-Tumour[,c(1,12)]
TLdf12<-Tumour[,c(1,13)]


#read in Wounds
Wounds<-read.csv("Wounds.csv")
#and save to have separate info for each season
Wf1<-Wounds[,c(1,2)]
Wf2<-Wounds[,c(1,3)]
Wf3<-Wounds[,c(1,4)]
Wf4<-Wounds[,c(1,5)]
Wf5<-Wounds[,c(1,6)]
Wf6<-Wounds[,c(1,7)]
Wf7<-Wounds[,c(1,8)]
Wf8<-Wounds[,c(1,9)]
Wf9<-Wounds[,c(1,10)]
Wf10<-Wounds[,c(1,11)]
Wf11<-Wounds[,c(1,12)]
Wf12<-Wounds[,c(1,13)]


#Read in Sex
Sex<-read.csv("SexTERGM.csv")

#read in Age
## AgeTERGM.csv not included in data
##Age<-read.csv("AgeTERGM.csv")

#-------------------------------------------------------------

#Convert matrices into networks
## note had to add as.matrix() to each f1 etc. otherwise get error
f1.net<-network(as.matrix(f1),directed=FALSE)
f2.net<-network(as.matrix(f2),directed=FALSE)
f3.net<-network(as.matrix(f3),directed=FALSE)
f4.net<-network(as.matrix(f4),directed=FALSE)
f5.net<-network(as.matrix(f5),directed=FALSE)
f6.net<-network(as.matrix(f6),directed=FALSE)
f7.net<-network(as.matrix(f7),directed=FALSE)
f8.net<-network(as.matrix(f8),directed=FALSE)
f9.net<-network(as.matrix(f9),directed=FALSE)
f10.net<-network(as.matrix(f10),directed=FALSE)
f11.net<-network(as.matrix(f11),directed=FALSE)
f12.net<-network(as.matrix(f12),directed=FALSE)

#Create a list of the seasonal networks to use in the models
networks<-list(f1.net,f2.net,f3.net,f4.net,f5.net,f6.net,f7.net,f8.net,f9.net,f10.net,f11.net,f12.net)

#And add sex and groups as fixed vertex attributes to these networks
for(i in 1:length(networks)){
  set.vertex.attribute(networks[[i]],
                       "Sex",
                       as.vector(as.numeric(Sex[,2])))
#  set.vertex.attribute(networks[[i]],
#                       "Age",
#                       as.vector(as.numeric(Age[,2])))
}

#Add DFTD status as a time-varying covariate to the three #networks in the list
set.vertex.attribute(networks[[1]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf1[,2])-1))
set.vertex.attribute(networks[[2]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf2[,2])-1))
set.vertex.attribute(networks[[3]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf3[,2])-1))
set.vertex.attribute(networks[[4]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf4[,2])-1))
set.vertex.attribute(networks[[5]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf5[,2])-1))
set.vertex.attribute(networks[[6]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf6[,2])-1))
set.vertex.attribute(networks[[7]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf7[,2])-1))
set.vertex.attribute(networks[[8]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf8[,2])-1))
set.vertex.attribute(networks[[9]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf9[,2])-1))
set.vertex.attribute(networks[[10]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf10[,2])-1))
set.vertex.attribute(networks[[11]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf11[,2])-1))
set.vertex.attribute(networks[[12]],
                     "DFTD",
                     as.vector(as.numeric(DFTDf12[,2])-1))


#Add Season as a time-varying covariate to the three #networks in the list
set.vertex.attribute(networks[[1]],
                     "Season",
                     as.vector(as.numeric(Seasf1[,2])-1))
set.vertex.attribute(networks[[2]],
                     "Season",
                     as.vector(as.numeric(Seasf2[,2])-1))
set.vertex.attribute(networks[[3]],
                     "Season",
                     as.vector(as.numeric(Seasf3[,2])-1))
set.vertex.attribute(networks[[4]],
                     "Season",
                     as.vector(as.numeric(Seasf4[,2])-1))
set.vertex.attribute(networks[[5]],
                     "Season",
                     as.vector(as.numeric(Seasf5[,2])-1))
set.vertex.attribute(networks[[6]],
                     "Season",
                     as.vector(as.numeric(Seasf6[,2])-1))
set.vertex.attribute(networks[[7]],
                     "Season",
                     as.vector(as.numeric(Seasf7[,2])-1))
set.vertex.attribute(networks[[8]],
                     "Season",
                     as.vector(as.numeric(Seasf8[,2])-1))
set.vertex.attribute(networks[[9]],
                     "Season",
                     as.vector(as.numeric(Seasf9[,2])-1))
set.vertex.attribute(networks[[10]],
                     "Season",
                     as.vector(as.numeric(Seasf10[,2])-1))
set.vertex.attribute(networks[[11]],
                     "Season",
                     as.vector(as.numeric(Seasf11[,2])-1))
set.vertex.attribute(networks[[12]],
                     "Season",
                     as.vector(as.numeric(Seasf12[,2])-1))



#Add Tumour Load as a time-varying covariate to the #networks in the list
set.vertex.attribute(networks[[1]],
                     "Tumour",
                     as.vector(as.numeric(TLdf1[,2])-1))
set.vertex.attribute(networks[[2]],
                     "Tumour",
                     as.vector(as.numeric(TLdf2[,2])-1))
set.vertex.attribute(networks[[3]],
                     "Tumour",
                     as.vector(as.numeric(TLdf3[,2])-1))
set.vertex.attribute(networks[[4]],
                     "Tumour",
                     as.vector(as.numeric(TLdf4[,2])-1))
set.vertex.attribute(networks[[5]],
                     "Tumour",
                     as.vector(as.numeric(TLdf5[,2])-1))
set.vertex.attribute(networks[[6]],
                     "Tumour",
                     as.vector(as.numeric(TLdf6[,2])-1))
set.vertex.attribute(networks[[7]],
                     "Tumour",
                     as.vector(as.numeric(TLdf7[,2])-1))
set.vertex.attribute(networks[[8]],
                     "Tumour",
                     as.vector(as.numeric(TLdf8[,2])-1))
set.vertex.attribute(networks[[9]],
                     "Tumour",
                     as.vector(as.numeric(TLdf9[,2])-1))
set.vertex.attribute(networks[[10]],
                     "Tumour",
                     as.vector(as.numeric(TLdf10[,2])-1))
set.vertex.attribute(networks[[11]],
                     "Tumour",
                     as.vector(as.numeric(TLdf11[,2])-1))
set.vertex.attribute(networks[[12]],
                     "Tumour",
                     as.vector(as.numeric(TLdf12[,2])-1))


#Add Wounds as a time-varying covariate to the #networks in the list
set.vertex.attribute(networks[[1]],
                     "Wounds",
                     as.vector(as.numeric(Wf1[,2])-1))
set.vertex.attribute(networks[[2]],
                     "Wounds",
                     as.vector(as.numeric(Wf2[,2])-1))
set.vertex.attribute(networks[[3]],
                     "Wounds",
                     as.vector(as.numeric(Wf3[,2])-1))
set.vertex.attribute(networks[[4]],
                     "Wounds",
                     as.vector(as.numeric(Wf4[,2])-1))
set.vertex.attribute(networks[[5]],
                     "Wounds",
                     as.vector(as.numeric(Wf5[,2])-1))
set.vertex.attribute(networks[[6]],
                     "Wounds",
                     as.vector(as.numeric(Wf6[,2])-1))
set.vertex.attribute(networks[[7]],
                     "Wounds",
                     as.vector(as.numeric(Wf7[,2])-1))
set.vertex.attribute(networks[[8]],
                     "Wounds",
                     as.vector(as.numeric(Wf8[,2])-1))
set.vertex.attribute(networks[[9]],
                     "Wounds",
                     as.vector(as.numeric(Wf9[,2])-1))
set.vertex.attribute(networks[[10]],
                     "Wounds",
                     as.vector(as.numeric(Wf10[,2])-1))
set.vertex.attribute(networks[[11]],
                     "Wounds",
                     as.vector(as.numeric(Wf11[,2])-1))
set.vertex.attribute(networks[[12]],
                     "Wounds",
                     as.vector(as.numeric(Wf12[,2])-1))


##############MODEL SET 1 - DFTD STATUS IN M/NON-M SEASON##############

#Split into mating/non-mating season

#Mating season

m1m<-btergm(networks[3:7]~edges+   #structural (like GLM intercept)                  
              memory(type="autoregression")+   #memory term (time dependent)
              nodefactor("Sex")+           #sex effect on no. of edges
              nodematch("Sex")+            #sex assortment
              nodecov("Wounds")+             #number of wounds
              nodecov("DFTD"),            #DFTD effect on no. of edges
            R=10000)

summary(m1m)


#Non-Mating season

m1n<-btergm(networks[c(1,2, 8:12)]~edges+   #structural (like GLM intercept)                  
              memory(type="autoregression")+   #memory term (time dependent)
              nodefactor("Sex")+           #sex effect on no. of edges
              nodematch("Sex")+            #sex assortment
              nodecov("Wounds")+             #number of wounds
              nodecov("DFTD"),            #DFTD effect on no. of edges
            R=10000)

summary(m1n)



##############MODEL SET 2 - TUMOUR LOAD IN M/NON-M SEASON##############

#Split into mating/non-mating season

#Mating season

m2m<-btergm(networks[3:7]~edges+   #structural (like GLM intercept)                  
              memory(type="autoregression")+   #memory term (time dependent)
              nodefactor("Sex")+           #sex effect on no. of edges
              nodematch("Sex")+            #sex assortment
              nodecov("Wounds")+             #number of wounds
              nodecov("Tumour"),            #DFTD effect on no. of edges
            R=10000)

summary(m2m)


#Non-Mating season

m2n<-btergm(networks[c(1,2, 8:12)]~edges+   #structural (like GLM intercept)                  
              memory(type="autoregression")+   #memory term (time dependent)
              nodefactor("Sex")+           #sex effect on no. of edges
              nodematch("Sex")+            #sex assortment
              nodecov("Wounds")+             #number of wounds
              nodecov("Tumour"),            #DFTD effect on no. of edges
            R=10000)

summary(m2n)





