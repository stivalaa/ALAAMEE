#!/bin/bash
#
# File:    reorderAlaamTextable.sh
# Author:  Alex Stivala
# Created: October 2022
#
# Based on EstimNetDicrected/sripts/reorderEstimnetTextable.sh (Dec. 2017);
# just had to change number of trail rows tailrows
#
# Read output of stochasticAproxEstimation2textableMultiModels and
# permute the table rows according to specified order, in order to
# present the rows in an order we determine as best for presentation.
# 
# Usage: reorderAlaamTextable.sh [-r|-m] <intable> <permutation>
#
# where <intable> is the input tex file and
#       <permutation> is a permutation of 0..n-1 e.g. 2 0 1
# if -r is specfied, this means input contains extra rows for TotalRuns
#    and ConvergedRuns
# if -m is specified, this means intput contains extra row for Mahalanobis
#    distance (for GoF output in stochastic approximation)
#
# E.g.:
#   reorderAlaamTextable.sh  ecoli_estimations.tex  1 5 4 2 3 0 9 10 7 6
#
# Output is to stdout
#
# Uses various GNU utils options on echo, etc.


# https://stackoverflow.com/questions/15639888/reorder-lines-of-file-by-given-sequence
# Usage: schwartzianTransform "A.txt" 2 0 1
function schwartzianTransform {
    local file="$1"
    shift
    local sequence="$@"
    echo -n "$sequence" | sed 's/[^[:digit:]][^[:digit:]]*/\
/g' | paste -d ' ' - "$file" | sort -n | sed 's/^[[:digit:]]* //'
}

if [ $# -lt 2 ]; then
  echo "Usage: $0 [-r|-m] <infile> <permutation>" >&2
  exit 1
fi
has_runs=0
has_mahal=0
if [ $1 = "-r" ]; then
  has_runs=1
  shift 1
elif [ $1 = "-m" ]; then
  has_mahal=1
  shift 1
fi

infile=$1
shift 1
permutation=$*


tmpfile=`mktemp`

nfields=`echo ${permutation} | wc -w`
nuniq=`echo ${permutation} | tr ' ' '\n' | sort -n | uniq | wc -w`

if [ $nuniq != $nfields ]; then
  echo Not a valid permutation: $nfields fields but $nuniq unique fields >&2
  exit 1
fi

# assume format of input latex table from stochasticApproxEstimation2textableMultiModels.sh
# 7 header rows and 2 trailer rows
headrows=7
if [ $has_runs -eq 1 ]; then
    tailrows=5
elif [ $has_mahal -eq 1 ]; then
    tailrows=4
else
    tailrows=2
fi
head -n${headrows} ${infile}
cat ${infile} | tail -n+`expr ${headrows} + 1` |head -n-${tailrows} > ${tmpfile}
nrows=`cat ${tmpfile} | wc -l`
if [ $nrows -ne $nfields ]; then
  echo Permutation has $nfields fields but table has $nrows rows >&2
  rm ${tmpfile}
  exit 1
fi
schwartzianTransform ${tmpfile} ${permutation} 
tail -n${tailrows} ${infile}

rm ${tmpfile}

