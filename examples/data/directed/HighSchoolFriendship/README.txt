SocioPatterns High school friendship network and node attributes
("metadata") downloaded from:

http://www.sociopatterns.org/datasets/high-school-contact-and-friendship-networks/

(release date Jul 15, 2015).

This network is the third dataset listed on that page:

Friendship-network_data_2013.csv.gz
"-The third data set corresponds to the directed network of reported friendships. Each line has the form “i j”, meaning that student i reported a friendship with student j."

metadata_2013.txt
"-Finally the metadata file contains a tab-separated list in which each line of the form “i Ci Gi” gives class Ci and gender Gi of the person having ID i."


Terms and conditions

http://creativecommons.org/licenses/by-nc-sa/3.0/

The data are distributed to the public under a Creative Commons Attribution-NonCommercial- ShareAlike license. When this data is used in published research or for visualization purposes, please cite the following paper:

R. Mastrandrea, J. Fournet, A. Barrat, Contact patterns in a high school: a comparison between data collected using wearable sensors, contact diaries and friendship surveys.  PLoS ONE 10(9): e0136497 (2015)



The highschool_friendship_arclist.net and highschool_friendship_catattr.txt
files are created from the originals using the
convert_highschoolfriendship_directed_network_to_pajek_ALAAMEE_format.R
R script which uses the igraph library. (output saved in
convert_highschoolfriendship_directed_network_to_pajek_ALAAMEE_format.out
to facilitate converting integer sex and class attributes back to original
if needed).

highschool_friendship_binattr.txt has 1 for male, created from
highschool_friendship_catattr.txt with:

cat highschool_friendship_catattr.txt | awk '{if (NR == 1) {print "male"} else {if ($2 == "NA") {print 0} else {print $2 - 1}}}' > highschool_friendship_binattr.txt

highschool_friendship_class2BIO3.txt is a binary attribute with 1 for in
class '2BIO3' created with:

cat highschool_friendship_catattr.txt | awk '{if (NR == 1) {print "2BIO3"} else {if ($1 == 3) {print 1} else {print 0}}}' > highschool_friendship_class2BIO3.txt

highschool_friendship_catattr_NA99999.txt is a categrocial attribute file
for MPNet with the "NA" value changed to 99999 as MPNet crashes if there
is a "NA" (or any string) that is not numeric.

cat highschool_friendship_catattr.txt |sed 's/NA/99999/g' > highschool_friendship_catattr_NA99999.txt

Results for ALAAM estimation with male as outcome attribute should look 
something like this (from MPNet):

Estimation
Observed graph statistics:
54.00	293.00	285.00	156.00	
...

Effects	Lambda	Parameter	Stderr	t-ratio	SACF
DensityA	2.0000	-0.6577	0.327	0.081	-0.050	*
SenderAttrA	2.0000	-0.0212	0.100	0.083	-0.058	
ReceiverAttrA	2.0000	-0.1415	0.104	0.083	-0.042	
ContagionArcA	2.0000	0.2433	0.068	0.082	-0.071	*


And results for ALAAM estimation with clas 2BIO3 as outcome attribute should
look something like this:


Effects	Lambda	Parameter	Stderr	t-ratio	SACF
DensityA	2.0000	-2.1949	0.702	-0.005	0.713	*
SenderAttrA	2.0000	-0.1929	0.225	0.067	0.764	
ReceiverAttrA	2.0000	-0.1796	0.269	0.068	0.760	
ContagionArcA	2.0000	0.6997	0.122	0.073	0.760	*


[Note was using MPNet_MelNet_20220827 as saved in
SWITCHDRIVE\Institution\USI\shared\ERGMXL\ALAAM\]

Citation:

Mastrandrea, R., Fournet, J., & Barrat, A. (2015). Contact patterns in a high school: a comparison between data collected using wearable sensors, contact diaries and friendship surveys. PloS one, 10(9), e0136497.


Citation for igraph:

Csardi G, Nepusz T: The igraph software package for complex network
research, InterJournal, Complex Systems
1695. 2006. http://igraph.org

ADS
Thu Feb 10 16:08:13 AEDT 2022




[Note using MPNet_MelNet_20220827 as saved in
SWITCHDRIVE\Institution\USI\shared\ERGMXL\ALAAM\]

Results with gender(male) as outcome with ContagionReciprocityA,ReciprocityA,
EgoIn2StarA, EgoOut2StarA, Mixed2StarA, Mixed2StarSourceA, Mixed2StarSinkA,
T1TA, T2TA, T3TA added:

Estimation
Observed graph statistics:
54.00	293.00	285.00	209.00	156.00	52.00	855.00	993.00	1713.00	1633.00	1584.00	785.00	438.00	267.00
x...
Effects	Lambda	Parameter	Stderr	t-ratio	SACF
DensityA	2.00	-0.18610245	0.68903882	0.01284990	-0.02308074	
SenderAttrA	2.00	-0.75325707	0.48112803	0.03439175	-0.05141173	
ReceiverAttrA	2.00	0.12402741	0.40156549	0.02758769	-0.05240066	
ReciprocityAttrA	2.00	0.12708631	0.44472789	0.01281538	-0.04802113	
ContagionArcA	2.00	0.65169504	0.33489776	0.02162548	-0.06984476	
ContagionReciprocityA	2.00	-0.89552154	0.73726813	0.00243467	-0.06193958	
EgoIn2StarA	1.00	0.09052266	0.11331841	0.02608482	-0.04301231	
EgoOut2StarA	2.00	0.28956576	0.14420149	0.04113059	-0.05909200	*
Mixed2StarA	2.00	-0.15419800	0.11149412	0.02637022	-0.05416778	
Mixed2StarSourceA	2.00	0.00694169	0.03873212	0.03603801	-0.04913245	
Mixed2StarSinkA	2.00	0.00807485	0.03567562	0.03232393	-0.04509179	
T1TA	2.00	-0.05293439	0.06789030	0.03776465	-0.03987146	
T2TA	2.00	0.03443244	0.08165996	0.02773772	-0.05955607	
T3TA	2.00	-0.02890496	0.05544353	0.00276291	-0.07940726	

GoF result with some additional statistics e.g. T1DA, T1UA, T1CA, T3CA
and also categorical effects for cateogrical attribute 'class'
(GoF is a better way to get just the observed statistics than running
estimation which can take a long time, if we are just interested in
the statistics this is easier):

Statistics	Observed	Mean	StdDev	t-ratio
DensityA	54.00000000	123.48400000	2.47906111	-28.02835301	#
SenderAttrA	293.00000000	646.27600000	5.81083677	-60.79606325	#
ReceiverAttrA	285.00000000	650.37300000	4.96043053	-73.65751785	#
ReciprocityAttrA	209.00000000	506.69600000	4.81555646	-61.81964693	#
ContagionArcA	156.00000000	635.49500000	8.34781259	-57.43959809	#
ContagionReciprocityA	52.00000000	248.11700000	3.60517836	-54.39869556	#
EgoIn2StarA	855.00000000	1875.19000000	4.06987715	-250.66850003	#
AlterIn2Star2A	408.00000000	1935.88500000	15.64147611	-97.68163752	#
EgoOut2StarA	993.00000000	1950.90000000	6.09081275	-157.26965164	#
AlterOut2Star2A	435.00000000	1838.00400000	16.81035348	-83.46070783	#
Mixed2StarA	1713.00000000	3667.66000000	9.67545348	-202.02257233	#
Mixed2StarSourceA	1633.00000000	3639.56700000	21.24978849	-94.42762222	#
Mixed2StarSinkA	1584.00000000	3666.81100000	9.88419339	-210.72139299	#
T1TA	785.00000000	1798.61400000	6.40460803	-158.26323726	#
T1DA	796.00000000	1796.87100000	7.52491588	-133.00759982	#
T1UA	775.00000000	1801.68500000	4.93090002	-208.21452392	#
T1CA	659.00000000	1623.50700000	5.69666139	-169.31092334	#
T2TA	438.00000000	1788.26300000	10.81433451	-124.85863075	#
T3TA	267.00000000	1779.09900000	15.56628405	-97.13936836	#
T3CA	62.00000000	535.35600000	4.85255232	-97.54784059	#
class_o->MatchA	227.00000000	497.79600000	4.44143941	-60.97032408	#
class_o->MismatchA	66.00000000	148.48000000	2.73598246	-30.14639214	#
class_o<-MatchA	221.00000000	500.65500000	3.74031750	-74.76771691	#
class_o<-MismatchA	64.00000000	149.71800000	2.16575068	-39.57888637	#
class_o<->MatchA	171.00000000	407.95500000	3.60180163	-65.78790955	#
class_o<->MismatchA	38.00000000	98.74100000	2.16608379	-28.04185147	#
sex_o->MatchA	156.00000000	381.38900000	4.57642644	-49.24999948	#
sex_o->MismatchA	137.00000000	264.88700000	2.71592176	-47.08788078	#
sex_o<-MatchA	156.00000000	385.06100000	4.02557810	-56.90139269	#
sex_o<-MismatchA	129.00000000	265.31200000	2.40180266	-56.75403832	#
sex_o<->MatchA	104.00000000	298.15200000	4.01159519	-48.39770481	#
sex_o<->MismatchA	105.00000000	208.54400000	2.14896812	-48.18312511	#
Mahalanobis distance = 1289568.00000000
Maximum qasi-autocorrelation in absolute value = 24.27239960
