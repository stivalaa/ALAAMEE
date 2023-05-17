#!/bin/bash
#
# File:    getbashtimes.sh
# Author:  Alex Stivala
# Created: May 2023
#
#
#
# getbashtimes.sh - get total time used from bash times output in seconds
#
# Usage: getbashtimes.sh  file_list
#
# file_list list of files containing in them output from bash 'times' builtin
# format e.g.
#
#0m0.004s 0m0.004s
#31m50.958s 0m1.580s
#
# Output, sum of all the elapsed times in seconds, one line per file, is
# to stdout
#
#

if [ $# -lt 1 ]; then
    echo "Usage: $0 file list" >&2
    exit 1
fi


for timesfile in $*
do
   total_seconds=0
   for elapsed in `grep '^[0-9][0-9]*m' $timesfile`
   do
      mindex=`expr index ${elapsed} 'm'`
      mindex=`expr $mindex - 1`
      mins=`expr substr ${elapsed} 1 ${mindex}`
      secindex=`expr $mindex + 2`
      sindex=`expr index ${elapsed} 's'`
      seclen=`expr ${sindex} - ${secindex}`
      secs=`expr substr ${elapsed} ${secindex} ${seclen}`
      total_seconds=`echo "$total_seconds + $mins * 60 + $secs" | bc -l`
   done
  total_seconds=`printf "%.0f" $total_seconds`
  printf '%d\n' ${total_seconds}
done

