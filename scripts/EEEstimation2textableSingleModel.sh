#!/bin/bash
#
# File:    EEEstimation2textableSingleModel.sh
# Author:  Alex Stivala
# Created: May 2023
#
# (Copied from estimnetdirectedEstimation2texttableSingleModel.sh March 2019)
#
# Read output of computeALAAMEECovariance.R with the estimate,
# estimated std. error and t-ratio computed from ALAAMEE results
# and build LaTeX table for one model (not using underset etc. for CI, 
# simpler format)
# 
# Usage: EEEstimation2textableSingleModel.sh [-t] estimationoutputfile
#         -t: Output plain (readable) text table instead of LaTeX
#
# E.g.:
#   EEEstimation2textableSingleModel.sh  estimation.out
#
# Output is to stdout
#
# Uses various GNU utils options on echo, etc.
#
# Note requires
#   \usepackage[T1]{fontenc}
# in LaTeX that includes the table so that the "< 0.001" is handled
# correctly otherwise "<" shows up as upside-down exclamation mark.


zSigma=2 # multiplier of estimated standard error for nominal 95% C.I.
tratioThreshold=0.3 # t-ratio must be <= this for significance

usage() { echo "usage: $0 [-t] estimation.out" >&2; exit 1; }

plaintext=0
while getopts "t" opt; do
    case "${opt}" in
        t)
            plaintext=1
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))
if [ $# -ne 1 ]; then
    usage
fi
estimationresults=$1

estimnet_tmpfile=`mktemp`

if [ $plaintext -eq 0 ]; then
    echo "% Generated by: $0 $*"
    echo "% At: " `date`
    echo "% On: " `uname -a`

    echo  '\begin{tabular}{lrrc}'
    # echo '\toprule'
    echo '\hline'
fi
if [ $plaintext -eq 0 ]; then
    echo 'Effect & Estimate & Std. error \\'
else
    printf '%40.40s  Estimate  Std. error\n' ' '
fi
if [ $plaintext -eq 0 ]; then
    echo '\hline'
    #echo '\midrule'
fi

# new version has results starting at line following "Pooled" at start
# of line (pooling the individual run estimates values printed earlier) and
# 5 columns:
# Effect   estimate   sd(theta)   est.std.err  t.ratio
# (and maybe *) plus
# TotalRuns and ConvergedRuns e.g.:
#Diff_completion_percentage -0.002270358 0.005812427 0.01295886 0.021386
#TotalRuns 2
#ConvergedRuns 2
# (see computeALAAMEECovariance.R)
# https://unix.stackexchange.com/questions/78472/print-lines-between-start-and-end-using-sed
# get lines from Pooled up to blank line (may be followed by further
# text e.g. note on GWActivity parameter interpretation) or end.
cat ${estimationresults} | sed -n -e '/^Pooled/,/^$/{//!p}'  | tr -d '*' | fgrep -vw AcceptanceRate |  awk '{print $1,$2,$4,$5}'  |  tr ' ' '\t' >> ${estimnet_tmpfile}

effectlist=`cat ${estimnet_tmpfile} | grep -wv ConvergedRuns | grep -wv TotalRuns |  awk '{print $1}' | sort | uniq`

any_bad_tratio=0
for effect in ${effectlist} ConvergedRuns TotalRuns
do
  if [ ${effect} = "ConvergedRuns" ]; then
    if [ $plaintext -eq 0 ]; then
      echo '\hline'                
    else
      echo
    fi
  fi
  if [ $plaintext -eq 0 ]; then
    echo -n "${effect} " | tr '_' ' '
  else
    printf '%40.40s' ${effect}
  fi
  if [ ${effect} = "ConvergedRuns" -o ${effect} = "TotalRuns" ]; then
        runs=`grep -w ${effect} ${estimnet_tmpfile} | awk '{print $2}'`
        if [ $plaintext -eq 0 ]; then
          echo -n " & ${runs} & &  "
        else
          printf '  %d' ${runs}
        fi
  else
        estimnet_point=`grep -w ${effect} ${estimnet_tmpfile} | awk '{print $2}'`
        estimnet_stderr=`grep -w ${effect} ${estimnet_tmpfile} | awk '{print $3}'`
        estimnet_tratio=`grep -w ${effect} ${estimnet_tmpfile} | awk '{print $4}'`
        if [ "${estimnet_point}" == "" ];  then
            if [ $plaintext -eq 0 ]; then
                echo -n " & ---"
            else
                printf '--'
            fi
        else 
            # bc cannot handle scientific notation so use sed to convert it 
            estimnet_lower=`echo "${estimnet_point} - ${zSigma} * ${estimnet_stderr}" | sed -e 's/[eE]+*/*10^/' | bc -l`
            estimnet_upper=`echo "${estimnet_point} + ${zSigma} * ${estimnet_stderr}" | sed -e 's/[eE]+*/*10^/' | bc -l`
            estimnet_point_unformat="${estimnet_point}"
            estimnet_point=`echo "${estimnet_point}" | sed -e 's/[eE]+*/*10^/'`
            estimnet_tratio=`echo "${estimnet_tratio}" | sed -e 's/[eE]+*/*10^/'`
            estimnet_stderr_unformat="${estimnet_stderr}"
            estimnet_stderr=`echo "${estimnet_stderr}" | sed -e 's/[eE]+*/*10^/'`
            ##echo AAA "${estimnet_point}">&2
            abs_estimate=`echo "if (${estimnet_point} < 0) -(${estimnet_point}) else ${estimnet_point}" | bc -l`
            abs_tratio=`echo "if (${estimnet_tratio} < 0) -(${estimnet_tratio}) else ${estimnet_tratio}" | bc -l`
            ##echo YYY ${abs_estimate} >&2
            ##echo QQQ ${abs_tratio} >&2
            ##echo XXX "${abs_tratio} <= ${tratioThreshold} && ${abs_estimate} > ${zSigma} * ${estimnet_stderr}" >&2
            bad_tratio=`echo "${abs_tratio} > ${tratioThreshold}" | bc -l`
            if [ ${bad_tratio} -ne 0 ]; then
                any_bad_tratio=1
            fi
            signif=`echo "${abs_tratio} <= ${tratioThreshold} && ${abs_estimate} > ${zSigma} * ${estimnet_stderr}" | bc -l`
            ##echo ZZZ ${signif} >&2
            ##echo WWWW `echo "${estimnet_stderr}" | awk '{printf("%g", $0)}'` >&2
            ##echo EEE `echo "${estimnet_stderr}" | awk '{printf("%d", sprintf("%g", $0)+0.0 < 0.001)}'` >&2
            format_stderr=`echo "${estimnet_stderr_unformat}" | awk '{printf("%s", (sprintf("%g", $0)+0.0 < 0.001 ? "< 0.001" : sprintf("%.4f", $0)))}'`
            #echo XXX ${estimnet_stderr_unformat} ${estimnet_stderr} ${format_stderr} >&2
            if [ $plaintext -eq 0 ]; then
                #if [ "${estimnet_point_unformat}" = "${estimnet_point}" ]; then
                  printf ' & %.4f & %s & ' ${estimnet_point_unformat} "${format_stderr} "
                #else
                #  printf ' & %s & %s & ' ${estimnet_point} "${format_stderr} "
                #fi
            else
                printf ' % 8.4f     %.4f     ' ${estimnet_point_unformat} ${estimnet_stderr_unformat}
            fi
            if [ ${signif} -ne 0 ]; then
                echo -n '*'
            fi
        fi
  fi
  if [ $plaintext -eq 0 ]; then
      echo '\\'
  else
      echo
  fi
done
 
if [ $plaintext -eq 0 ]; then
    echo '\hline'
#echo '\bottomrule'
    echo '\end{tabular}'
fi

if [ $plaintext -eq 1 ]; then
    if [ ${any_bad_tratio} -ne 0 ]; then
        echo
        echo  "WARNING: One or more parameters had an EE algorithm t-ratio value"
        echo  "greater than ${tratioThreshold} in magnitude. Possibly the estimation did not converge"
        echo  "(check diagnostic plots) or the model is degenerate."
    fi
    echo "${effectlist}" | grep -q 'GWActivity\|GWSender\|GWReceiver'
    if [ $? -eq 0 ] ; then
        printf '\nNote: model contains one or more of the GWActivity, GWSender or GWReceiver\nparameters, which are not straightforward to interpret. Please read (and cite)\nthis paper for guidance:\n\n'
        printf '  Stivala, A. (2023). Overcoming near-degeneracy in the autologistic actor\n  attribute model. arXiv preprint arXiv:2309.07338.\n  https://arxiv.org/abs/2309.07338\n\n'
    fi
fi

rm ${estimnet_tmpfile}
