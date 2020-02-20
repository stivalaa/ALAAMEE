#!/bin/sh

time python ../../python/runALAAMEEkarateClub.py

Rscript ../../R/plotALAAMEESimpleDemoResults.R  theta_values_karate.txt  dzA_values_karate.txt

