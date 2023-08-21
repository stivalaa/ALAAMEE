#!/bin/bash


echo -n "started at: "; date
uname -a

time Rscript $DOCUMENTS/USI//ALAAMEE/R/convertSNAPpokecToALAAMEEFormat.R 1000 
##all nodes, does not converge on alaam (like ergm): time Rscript $HOME/ALAAMEE/R/convertSNAPpokecToALAAMEEFormat.R 

echo -n "ended at: "; date
