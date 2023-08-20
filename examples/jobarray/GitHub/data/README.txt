GitHub Social Network downloaded from

http://snap.stanford.edu/data/github-social.html
http://snap.stanford.edu/data/git_web_ml.zip

on 12 April 2021.

Note not included in repository as large, download to here from SNAP
address above and run script to extract.

ADS

Info from SNAP (http://snap.stanford.edu/data/github-social.html):

GitHub Social Network
Dataset information

A large social network of GitHub developers which was collected from the public API in June 2019. Nodes are developers who have starred at least 10 repositories and edges are mutual follower relationships between them. The vertex features are extracted based on the location, repositories starred, employer and e-mail address. The task related to the graph is binary node classification - one has to predict whether the GitHub user is a web or a machine learning developer. This target feature was derived from the job title of each user.

MUSAE paper: https://arxiv.org/abs/1909.13021
MUSAE Project: https://github.com/benedekrozemberczki/MUSAE


Dataset statistics
Directed	No.
Node features	Yes.
Edge features	No.
Node labels	Yes. Binary-labeled.
Temporal	No.
Nodes	37,700
Edges	289,003
Density	0.001
Transitvity	0.013

Possible tasks
Binary node classification
Link prediction
Community detection
Network visualization

Source (citation)
B. Rozemberczki, C. Allen and R. Sarkar. Multi-scale Attributed Node Embedding. 2019.

          @misc{rozemberczki2019multiscale,
            title={Multi-scale Attributed Node Embedding},
            author={Benedek Rozemberczki and Carl Allen and Rik Sarkar},
            year={2019},
            eprint={1909.13021},
            archivePrefix={arXiv},
            primaryClass={cs.LG}
        }
        

Files
File 	Description
git_web_ml.zip http://snap.stanford.edu/data/git_web_ml.zip 	GitHub Social Network
