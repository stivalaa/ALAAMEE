#!/bin/sh

time python ./runALAAMEEkarateClub.py

Rscript ./plotALAAMEESimpleDemoResults.R  theta_values_karate.txt  dzA_values_karate.txt

