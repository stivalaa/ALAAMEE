#!/bin/bash
#
# File:    stochasticApproxGoF2textableMultiModels.sh
# Author:  Alex Stivala
# Created: October 2022
#
#
# Read output of estimateALAAMSA.run_on_network_attr() with
# to get goodness-of-fit t-ratios computed after Stochastic
# Approximation algorithm for ALAAM and build LaTeX table for multiple
# different models
# 
# Usage: stochasticApproxGoF2textableMultiModels.sh estimationoutputfile_model1 estimationoutputfile_model2 ...
#
# E.g.:
#   stochasticApproxGoF2textableMultiModels.sh  estimation.out model2/estimation.out
#
# Output is to stdout
#
# Uses various GNU utils options on echo, etc.

tratioThreshold=0.1 # t-ratio larger than this is put in bold


if [ $# -lt 1 ]; then
    echo "usage: $0 estimation1.out estimation2.out ..." >&2
    exit 1
fi

num_models=`expr $#`

tmpfile=`mktemp`

echo "% Generated by: $0 $*"
echo "% At: " `date`
echo "% On: " `uname -a`

echo -n '\begin{tabular}{l'
i=1
while [ $i -le $num_models ]
do
  echo -n r
  i=`expr $i + 1`
done
echo '}'
echo '\hline'  
echo -n 'Effect '
i=1
while [ $i -le $num_models ]
do
  echo -n " & Model $i"
  i=`expr $i + 1`
done
echo '\\'
echo '\hline'  

#
# Estimation output looks like this:
#...
#                                 t-ratio
#              bipartiteDensityA   0.067
#             bipartiteActivityA   0.050
#           bipartiteEgoTwoStarA   0.028
#         bipartiteEgoThreeStarA   0.038
#        bipartiteAlterTwoStar1A   0.050
#        bipartiteAlterTwoStar2A   0.062
#           bipartiteFourCycle1A  -0.023
#           bipartiteFourCycle2A  -0.017
#                        age_oOc  -0.015
#               notAustralia_oOb  -0.051
#              logMarketCap_o_Oc   0.051
#               ListingYear_o_Oc   0.051
#              notAustralia_o_Ob  -0.046
#               country_oO_Odiff   0.005
#                betweenness_oOc   0.020
#   industryGroup.Materials_o_Ob   0.018
#       industryGroup.Banks_o_Ob   0.015
#                       Two-Star   0.028
#                     Three-Star   0.038
#                   Alter-2Star1   0.050
#                      Contagion     nan
#                   Alter-2Star2   0.062
#               Partner-Activity     nan
#               Partner-Resource     nan
#
# twoPaths cache info:  CacheInfo(hits=0, misses=0, maxsize=None, currsize=0)
#
# We will parse from after the "                t-ratio" header line to get
# parameter names and t-ratios.
#


model=1
for estimationresults in $*
do
    cat ${estimationresults} | sed -n -e '/^[[:space:]]*t-ratio$/,/^$/{p}' | sed '1d;$d'  | fgrep -vw 'Estimate' | awk '{print $1,$2}'  |  tr ' ' '\t' | sed "s/^/${model}\t/" >> ${tmpfile}
    model=`expr $model + 1`
done


effectlist=`cat ${tmpfile} | awk '{print $2}' | sort | uniq`

for effect in ${effectlist}
do
    model=1
    echo -n "${effect} " | tr '_' ' '
    while [ $model -le $num_models ]; 
    do
        tratio=`grep -w ${effect} ${tmpfile} | awk -vmodel=$model '$1 == model {print $3}'`
        if [ "${tratio}" = "" ];  then
            echo -n " & ---"
        elif [ "${tratio}" = "nan" ];  then
            echo -n " & ---"
        else
            abs_tratio=`echo "if (${tratio} < 0) -(${tratio}) else ${tratio}" | bc -l`
            good_fit=`echo "${abs_tratio} < ${tratioThreshold}" | bc -l`
            if [ $good_fit -eq 1 ]; then
                printf ' & $%.3f$' ${tratio}
            else
                printf ' & $\\mathbf{%.3f}$' ${tratio}
            fi
        fi
        model=`expr $model + 1`
    done
    echo '\\'
done

echo '\hline'  
echo '\end{tabular}'

rm ${tmpfile}