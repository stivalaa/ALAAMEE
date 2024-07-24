# ALAAMEE

Autologistic Actor Attribute Model (ALAAM) parameter estimation using Equilibrium Expectation (EE) algorithm. Also includes an implementation of the Robbins-Monro stochastic approximation algorithm for estimating ALAAM parameters, and functions for simulation and goodness-of-fit tests.

The ALAAM is a social influence model. Parameters of the model are estimated that maximize the likelihood of an observed binary outcome for each node, given a social network and nodal attributes, allowing the outcome on other nodes to influence a node's outcome.

This software is applicable to one-mode networks (directed or undirected), and undirected two-mode (bipartite) networks. It allows for estimation from network snowball samples (Stivala et al., 2020), and includes "geometrically weighted" statistics for avoiding near-degeneracy in larger networks (Stivala, 2023).

This Python implementation uses the [NumPy](https://numpy.org/) library for vector and matrix data types and functions. In addition, there are R scripts for estimating standard errors and plotting results from the output.

## Citing

If you use this software in your research, please cite:

Stivala, A., Wang, P., & Lomi, A. (2024). ALAAMEE: Open-source software for fitting autologistic actor attribute models. arXiv preprint arXiv:2404.03116. https://arxiv.org/abs/2404.03116

## Other ALAAM software

* For the original Windows GUI implementation using stochastic approximation, for one-mode, two-mode, and multilevel networks, [MPNet](http://www.melnet.org.au/pnet).
* For a Bayesian version handling missing data and sampled networks (Koskinen & Daraganova, 2022), implemented in R, https://github.com/johankoskinen/ALAAM

## Funding

Development of the ALAAMEE software was funded by the Swiss National Science Foundation project numbers 167326 (NRP 75) and 200778.

## References

Borisenko, A., Byshkin, M., & Lomi, A. (2019). A Simple Algorithm for Scalable Monte Carlo Inference. arXiv preprint arXiv:1901.00533. https://arxiv.org/abs/1901.00533

Byshkin, M., Stivala, A., Mira, A., Robins, G., & Lomi, A. (2018). [Fast Maximum Likelihood Estimation via Equilibrium Expectation for Large Network Data](https://www.nature.com/articles/s41598-018-29725-8). *Scientific Reports* 8:11509. https://doi.org/10.1038/s41598-018-29725-8

Daraganova, G., & Robins, G. (2013). Autologistic actor attribute models. In D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge University Press, New York.

Koskinen, J., & Daraganova, G. (2022). [Bayesian analysis of social influence](https://rss.onlinelibrary.wiley.com/doi/10.1111/rssa.12844). *Journal of the Royal Statistical Society Series A*. 185(4), 1855-1881. https://doi.org/10.1111/rssa.12844

Parker, A., Pallotti, F., & Lomi, A. (2022). New network models for the analysis of social contagion in organizations: an introduction to autologistic actor attribute models. *Organizational Research Methods*, 25(3), 513–540. https://doi.org/10.1177/10944281211005167

Robins, G., Pattison, P., & Elliott, P. (2001). Network models for social influence processes. *Psychometrika*, 66(2), 161-189. https://link.springer.com/article/10.1007/BF02294834

Snijders, T. A. B. (2002). [Markov chain Monte Carlo estimation of exponential random graph models](https://www.cmu.edu/joss/content/articles/volume3/Snijders.pdf). *Journal of Social Structure*, 3(2), 1-40.

Stivala, A. (2023). Overcoming near-degeneracy in the autologistic actor attribute model. arXiv preprint arXiv:2309.07338. https://arxiv.org/abs/2309.07338

Stivala, A. D., Gallagher, H. C., Rolls, D. A., Wang, P., & Robins, G. L. (2020). Using Sampled Network Data With The Autologistic Actor Attribute Model. arXiv preprint arXiv:2002.00849. https://arxiv.org/abs/2002.00849

Stivala, A., Robins, G., & Lomi, A. (2020). Exponential random graph model parameter estimation for very large directed networks. *PloS ONE*, 15(1), e0227804. https://arxiv.org/abs/1904.08063

Stivala, A., Wang, P., & Lomi, A. (2024). ALAAMEE: Open-source software for fitting autologistic actor attribute models. arXiv preprint arXiv:2404.03116. https://arxiv.org/abs/2404.03116

Wang, P., Robins, G., & Pattison, P. (2009). PNet: A program for the simulation and estimation of exponential random graph  models. University of Melbourne. http://www.melnet.org.au/s/PNetManual.pdf

Wang, P., Robins, G., Pattison, P., & Koskinen, J. (2014). MPNet: A program for the simulation and estimation of exponential random graph models for multilevel networks. University of Melbourne. http://www.melnet.org.au/s/MPNetManual.pdf

Wang, P., Stivala, A., Robins, G.,Pattison, P., Koskinen, J., & Lomi, A. (2022) PNet: Program for the simulation and estimation of exponential random graph models for multilevel networks.  http://www.melnet.org.au/s/MPNetManual2022.pdf
