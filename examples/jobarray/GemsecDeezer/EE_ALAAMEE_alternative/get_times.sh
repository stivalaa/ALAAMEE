#!/bin/sh

# get elapsed time in minutes and make histogram, saving times in minutes to file

#WARNING: overwritten

country=ro
echo ${country}
outfile=jobtimes_${country}.txt
hist_outfile=jobtimes_${country}_histogram.txt

../../../../scripts/getbashtimes.sh  alaamee_GEMSEC_Deezer_RO-59288253_*.out| awk '{print $1 / 60}'  >  ${outfile}

# histogram.py does not work on OzSTAR as it requires python 2 so use 
# histogram.sh intead to load thie python 2 module
cat ${outfile} | histogram.sh | tee ${hist_outfile}

country=hr
echo ${country}
outfile=jobtimes_${country}.txt
hist_outfile=jobtimes_${country}_histogram.txt

../../../../scripts/getbashtimes.sh alaamee_GEMSEC_Deezer_HR-59288119_*.out| awk '{print $1 / 60}'  >  ${outfile}

# histogram.py does not work on OzSTAR as it requires python 2 so use 
# histogram.sh intead to load thie python 2 module
cat ${outfile} | histogram.sh | tee ${hist_outfile}

country=hu
echo ${country}
outfile=jobtimes_${country}.txt
hist_outfile=jobtimes_${country}_histogram.txt

../../../../scripts/getbashtimes.sh alaamee_GEMSEC_Deezer_HU-59288200_*.out  | awk '{print $1 / 60}'  >  ${outfile}

# histogram.py does not work on OzSTAR as it requires python 2 so use 
# histogram.sh intead to load thie python 2 module
cat ${outfile} | histogram.sh | tee ${hist_outfile}
