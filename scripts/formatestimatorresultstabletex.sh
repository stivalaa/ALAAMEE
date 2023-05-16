#!/bin/sh
#
# File:    formatestimatorresultstabletex.sh
# Author:  Alex Stivala
# Created: November 2013
#
#
# get rows of table output from makeMLEresultstable.R and add
# LaTeX header/footer
# 
# Input is stdin
#
# Usage: formatestimatorresultstabletex.sh estimatorresutlstablefile.txt
#
# E.g.:
#    formatestimatorresultstabletex.sh  estimator_error_statistics.txt
#
# Output is to stdout.
#
# Uses various GNU utils options on  echo &  etc.


# write_header() - write LaTeX table header for ALAAMEE table 
# to stdout
write_header() {
  cat <<EOF
\begin{tabular}{lrrrrrrr}
\hline
Effect &  Bias &  RMSE &  Mean           & Std. dev.   & Total    &   Mean     &  Total \\\\
       &       &       &  standard       &   estimate  & samples & runs       &  runs per \\\\
       &       &       &  error          &             & converged& converged  &  sample  \\\\
\hline
EOF
}

if [ $# -ne 1 ]; then
  echo "Usage: $0 error_statistics.txt" >&2
  exit 1
fi
infile=$1


write_header

grep ALAAMEE $infile | awk -F\& -vOFS=\& '{printf("%s & %s & %5.4f & %5.4f & %5.4f & %5.4f & %d & %0.2f & %g \\\\\n", $3,$5,$6,$7,$9,$10,$15,$11,$16)}' | sed 's/ALAAMEE  &//g' | sed 's/binary oOb/Binary/g' | sed 's/continuous oOc/Continuous/g'

cat <<EOF
\hline
\end{tabular}
EOF
