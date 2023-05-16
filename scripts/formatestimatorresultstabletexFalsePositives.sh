#!/bin/sh
#
# File:    formatestimatorresultstabletexFalsePositives.sh
# Author:  Alex Stivala
# Created: December 2013
#
#
# get rows of table output from makeMLEresultstable.R and add
# LaTeX header/footer
# 
# Input is stdin
#
# Usage: formatestimatorresultstabletexFalsePositvies.sh estimatorresutlstablefile.txt
#
# E.g.:
#    formatestimatorresultstabletex.sh  estimator_error_false_positives_statistics.txt
#
# Output is to stdout
#
# Uses various GNU utils options on  echo &  etc.


# write_header() - write LaTeX table header for EstimNetDirected
write_header() {
  cat <<EOF 
\begin{tabular}{lrrrrrrrrr}
\hline
Effect &  Bias &  RMSE &  \multicolumn{3}{c}{False positive rate (\%)}  & in C.I.    & Total     & Mean       & Total\\\\
       &       &       &   Estim. & \multicolumn{2}{c}{95\% C.I.}       &  (\%)      & samples  & runs       & runs per\\\\
       &       &       &   & lower & upper                              &            & converged & converged  & sample\\\\
\hline
EOF
}


if [ $# -ne 1 ]; then
  echo "Usage: $0 error_statistics.txt" >&2
  exit 1
fi
infile=$1



write_header

# the --posix flag on awk (gawk) stop it converting NaN and Inf to 0
# then sed 's/nan/--/g' actuall converts to --- as it has written nan as -nan
grep ALAAMEE $infile | awk --posix -F\& -vOFS=\& '{ if ($9 != " NA ") printf("%s & %s & %5.4f & %5.4f & %2.0f & %2.0f & %2.0f & %2.0f & %d & %2.2f & %g\\\\\n",$3,$5,$7,$8,$9,$13,$14,$18,$16,$12,$17)}' | sed 's/nan/--/g'  | sed 's/ ALAAMEE  &//g'   | sed 's/binary oOb/Binary/g' | sed 's/continuous oOc/Continuous/g'

cat <<EOF
\hline
\end{tabular}
EOF
