#!/bin/sh

time python ./runALAAMEESimpleDemo.py

Rscript ./plotALAAMEESimpleDemoResults.R  theta_values_n500_kstar_simulate12750000.txt  dzA_values_n500_kstar_simulate12750000.txt

