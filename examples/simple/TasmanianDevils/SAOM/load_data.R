## R code to load data sets copied from TERGM_code.txt 
## and changed to load from ../tergm_replication/ directory

#read in matrices

f1<-read.csv("../tergm_replication/f1.csv")
names<-f1[,1]
f1<-sign(f1[,2:ncol(f1)])
rownames(f1)<-colnames(f1)<-names

f2<-read.csv("../tergm_replication/f2.csv")
names<-f2[,1]
f2<-sign(f2[,2:ncol(f2)])
rownames(f2)<-colnames(f2)<-names

f3<-read.csv("../tergm_replication/f3.csv")
names<-f3[,1]
f3<-sign(f3[,2:ncol(f3)])
rownames(f3)<-colnames(f3)<-names

f4<-read.csv("../tergm_replication/f4.csv")
names<-f4[,1]
f4<-sign(f4[,2:ncol(f4)])
rownames(f4)<-colnames(f4)<-names

f5<-read.csv("../tergm_replication/f5.csv")
names<-f5[,1]
f5<-sign(f5[,2:ncol(f5)])
rownames(f5)<-colnames(f5)<-names

f6<-read.csv("../tergm_replication/f6.csv")
names<-f6[,1]
f6<-sign(f6[,2:ncol(f6)])
rownames(f6)<-colnames(f6)<-names

f7<-read.csv("../tergm_replication/f7.csv")
names<-f7[,1]
f7<-sign(f7[,2:ncol(f7)])
rownames(f7)<-colnames(f7)<-names

f8<-read.csv("../tergm_replication/f8.csv")
names<-f8[,1]
f8<-sign(f8[,2:ncol(f8)])
rownames(f8)<-colnames(f8)<-names

f9<-read.csv("../tergm_replication/f9.csv")
names<-f9[,1]
f9<-sign(f9[,2:ncol(f9)])
rownames(f9)<-colnames(f9)<-names

f10<-read.csv("../tergm_replication/f10.csv")
names<-f10[,1]
f10<-sign(f10[,2:ncol(f10)])
rownames(f10)<-colnames(f10)<-names

f11<-read.csv("../tergm_replication/f11.csv")
names<-f11[,1]
f11<-sign(f11[,2:ncol(f11)])
rownames(f11)<-colnames(f11)<-names

f12<-read.csv("../tergm_replication/f12.csv")
names<-f12[,1]
f12<-sign(f12[,2:ncol(f12)])
rownames(f12)<-colnames(f12)<-names



#-------------------------------------------------------------

#read in DFTD status
DFTD<-read.csv("../tergm_replication/DFTDstatus.csv")
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
Season<-read.csv("../tergm_replication/Season.csv")
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
Tumour<-read.csv("../tergm_replication/TumourLoad_factor.csv")
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
Wounds<-read.csv("../tergm_replication/Wounds.csv")
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
Sex<-read.csv("../tergm_replication/SexTERGM.csv")

#read in Age
## AgeTERGM.csv not included in data
##Age<-read.csv("../tergm_replication/AgeTERGM.csv")
