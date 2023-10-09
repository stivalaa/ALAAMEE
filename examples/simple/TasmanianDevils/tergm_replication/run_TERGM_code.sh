#!/bin/sh

time R --vanilla --no-restore --file=TERGM_code.R > TERGM_code.out  2>&1

# Not using Rscript as then the output does not actually appear when stdout redirected
