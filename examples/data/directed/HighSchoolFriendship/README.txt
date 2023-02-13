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

Results with gender(male) as outcome with ContagionReciproticyA added:

Estimation
Observed graph statistics:
54.00	293.00	285.00	156.00	52.00
...
Effects	Lambda	Parameter	Stderr	t-ratio	SACF
DensityA	2.00	-0.87259214	0.35085574	-0.04779465	-0.01505060	*
SenderAttrA	2.00	0.02181337	0.11645857	-0.05923215	-0.03062335	
ReceiverAttrA	2.00	-0.16110183	0.11999184	-0.06581364	-0.01855918	
ContagionArcA	2.00	0.67158579	0.15392191	-0.04594921	-0.06160798	*
ContagionReciprocityA	2.00	-1.08829738	0.38851211	-0.02489552	-0.05194178	*



And now with ReciprocityA also added:

Estimation
Observed graph statistics:
54.00	293.00	285.00	209.00	156.00	52.00
...
Effects	Lambda	Parameter	Stderr	t-ratio	SACF
DensityA	2.00	-0.91909780	0.36185488	0.01372661	-0.03629518	*
SenderAttrA	2.00	0.08108040	0.20822941	-0.02294572	-0.04941755	
ReceiverAttrA	2.00	-0.11039417	0.23853906	0.00078327	-0.04426219	
ReciprocityAttrA	2.00	-0.11882264	0.44608587	-0.01755387	-0.04897276	
ContagionArcA	2.00	0.59814988	0.30826921	0.01731254	-0.04011905	
ContagionReciprocityA	2.00	-0.92350718	0.71902349	0.01781853	-0.05401591	
