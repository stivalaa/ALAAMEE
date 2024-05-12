#
# File:    simualateALAAM.py
# Author:  Alex Stivala
# Created: May 2020
#
"""Python implementation of ALAAM simulation (generating binary outcome
   vectors given network, node attributes, ALAAM mode parmaters).

 The ALAAM is described in:

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.


 The example data is described in:

  Stivala, A. D., Gallagher, H. C., Rolls, D. A., Wang, P., & Robins,
  G. L. (2020). Using Sampled Network Data With The Autologistic Actor
  Attribute Model. arXiv preprint arXiv:2002.00849.

"""
import sys,os
import numpy as np         # used for matrix & vector data types and functions

from Graph import Graph,NA_VALUE
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
from changeStatisticsALAAM import *
from basicALAAMsampler import basicALAAMsampler
from computeObservedStatistics import computeObservedStatistics



def rand_bin_array(K, N):
    """rand_bin_array - binary vector of length N with exactly K ones
                        at random indices

    Parameters:
        K  - number of ones
        N  - length of vector

    Return value:
       numpy array of length N with K ones at random positions (others 0)

    https://stackoverflow.com/questions/19597473/binary-random-array-with-a-specific-proportion-of-ones
    """
    arr = np.zeros(N)
    arr[:K]  = 1
    np.random.shuffle(arr)
    return arr



def simulateALAAM(G, changestats_func_list, theta, numSamples,
                  iterationInStep = None, burnIn = None,
                  sampler_func = basicALAAMsampler, Ainitial = None,
                  bipartiteFixedMode = None, Aobs = None):
    """
    Simulate ALAAM (generate binary outcome vector) given model parameters
    and network (including node attributes).
    This is a generator function (i.e. use it as an iterator).


    Parameters:
       G                   - Graph object for graph to simulate ALAAM on
       changestats_func_list-list of change statistics funcions
       theta               - corresponding vector of theta values
       numSamples          - number of samples to yield
       iterationInStep     - number of sampler iterations 
                             i.e. the number of iterations between samples
                             (or 10*numNodes if None)
       burnIn              - number of samples to discard at start
                             (or 10*iterationInStep if None)
       sampler_func        - ALAAM sampler function with signature
                             (G, A, changestats_func_list, theta, performMove,
                              sampler_m); see basicALAAMsampler.py
                             default basicALAAMsampler
       Ainitial              - vector of 0/1 outcome variables to initialize
                               the outcome vector to before simulation process,
                               rather than starting from all 0 or random.
                               Default None, for random initialization here.
      bipartiteFixedMode - for bipartite networks only, the mode
                                 (MODE_A or MODE_B that is fixed to NA
                                 in simulation, for when outcome
                                 variable not defined for that mode,
                                 or None. Default None.
      Aobs                 - vector of 0/1 observed outcome variables for ALAAM
                             for use with snowball conditional estimation only,
                             or None (default None).

     Returns:
       This is a generator function that yields tuple
        (A, stats, acceptance_Rate, t) where
          A is vector of 0/1 ALAAM outcome and
          stats is vector of the model sufficient statistics
          acceptance_rate is the sampler acceptance rate
          t is the iteration number
       values on each call.
    """
    bipartite = isinstance(G, BipartiteGraph)
    assert len(theta) == len(changestats_func_list)
    assert bipartiteFixedMode in [None, MODE_A, MODE_B]
    assert not (bipartiteFixedMode is not None and not bipartite)
    assert not (G.zone is not None and bipartite)


    if iterationInStep is None:
        iterationInStep = 10 * G.numNodes()

    if burnIn is None:
        burnIn = 10*iterationInStep

    if Ainitial is not None:
        A = np.copy(Ainitial)
    else:
        START_FROM_ZERO = False 
        if START_FROM_ZERO: # start from zero vector
            A = np.zeros(G.numNodes())  # initialize outcmoe vector to zero
        else:   # do not use all zero,to avoid special case of proposal probability
            if G.zone is not None: # snowball conditional estimation
                # For snowball conditional estimation, we must not start with
                # random initial outcome vector, but rather make sure the
                # nodes in the outermost zone have the same outcome attributes
                # as the obseved vector
                A= np.copy(Aobs) # copy of observed vector
                # make vector of 50% ones, size of number of inner nodes
                Arandom_inner = rand_bin_array(int(0.5*len(G.inner_nodes)), len(G.inner_nodes))
                # set the outcome for inner nodes to random values, leaving
                # value of outermost nodes at the original observed values
                A[G.inner_nodes] = Arandom_inner
            elif bipartite:
                # initialize outcome vector to all NA for one mode and
                # 50% zero for other mode, depending which mode we want fixed
                # to all NA values.
                if bipartiteFixedMode == MODE_B:
                    A = np.concatenate(
                        (rand_bin_array(int(0.5*G.num_A_nodes), G.num_A_nodes),
                          np.ones(G.num_B_nodes)*NA_VALUE) )
                elif bipartiteFixedMode == MODE_A:
                    A = np.concatenate(
                        (np.ones(G.num_A_nodes)*NA_VALUE,
                       rand_bin_array(int(0.5*G.num_B_nodes), G.num_B_nodes)) )
                else:
                    # initialize outcome vector to 50% ones
                    A = rand_bin_array(int(0.5*G.numNodes()), G.numNodes())
            else:
                # initialize outcome vector to 50% ones
                A = rand_bin_array(int(0.5*G.numNodes()), G.numNodes())

    # And compute observed statistics by summing change stats for each
    # 1 variable (note if instead starting at all zero A vector don't
    # have to do this as then Z is zero vector)

    Z = computeObservedStatistics(G, A, changestats_func_list)

    (acceptance_rate,
     changeTo1ChangeStats,
     changeTo0ChangeStats) = sampler_func(G, A,
                                          changestats_func_list,
                                          theta,
                                          performMove = True,
                                          sampler_m = burnIn)
    Z += changeTo1ChangeStats - changeTo0ChangeStats

    for i in range(numSamples):
        (acceptance_rate,
         changeTo1ChangeStats,
         changeTo0ChangeStats) = sampler_func(G, A,
                                              changestats_func_list,
                                              theta,
                                              performMove = True,
                                              sampler_m = iterationInStep)
        Z += changeTo1ChangeStats - changeTo0ChangeStats
        yield (np.array(A), np.array(Z), acceptance_rate, (i+1)*iterationInStep+burnIn)




def simulate_from_network_attr(arclist_filename, param_func_list, labels,
                               theta,
                               binattr_filename=None,
                               contattr_filename=None,
                               catattr_filename=None,
                               sampler_func = basicALAAMsampler,
                               numSamples = 100,
                               iterationInStep = None,
                               burnIn = None,
                               zone_filename = None,
                               directed = False,
                               bipartite = False,
                               degreestats = False,
                               outputSimulatedVectors = False,
                               simvecFilePrefix = "sim_outcome",
                               Ainitial = None,
                               bipartiteFixedMode = None):
    """Simulate ALAAM from on specified network with binary and/or continuous
    and categorical attributes.

    Parameters:
         arclist_filename - filename of Pajek format arclist
         param_func_list   - list of change statistic functions corresponding
                             to parameters to estimate
         labels            - list of strings corresponding to param_func_list
                             to label output (header line)
         theta             - correponding vector of theta values
         binattr_filename - filename of binary attributes (node per line)
                            Default None, in which case no binary attr.
         contattr_filename - filename of continuous attributes (node per line)
                            Default None, in which case no continuous attr.
         catattr_filename - filename of categorical attributes (node per line)
                            Default None, in which case no categorical attr.
         sampler_func        - ALAAM sampler function with signature
                               (G, A, changestats_func_list, theta, performMove,
                                sampler_m); see basicALAAMsampler.py
                               default basicALAAMsampler
         iterationInStep  - number of sampler iterations
                             i.e. the number of iterations between samples
                             (or 10*numNodes if None)
         numSamples       - Number of samples (default 100)
         burnIn           - Number of sampels to discard at start
                            (or 10*iterationInStep if None)
         zone_filename   - filename of snowball sampling zone file
                           (header line 'zone' then zone number for nodes,
                           one per line)
                           Default None, in which case no snowball zones.
                           If not None then the sampler_func should take
                           account of snowball sample zones i.e.
                           conditionalALAAMsampler()
         directed        - Default False.
                           True for directed network else undirected.
         bipartite       - Default False.
                           True for two-mode network else one-mode.
         degreestats     - Default False.
                           If True then also compute mean and variance
                           of nodes with outcome variable = 1 (and also 0).
         outputSimulatedVectors - if True, output each simulated vector
                                as a file with single column with header
                                line 'outcome' and each subsequent line
                                0 or 1 (or NA) for outcome binary value
                                for each node (i.e. same format as
                                observed outcome binary vector as used
                                in estimation functions like
                                estimateALAAMEE.run_on_network_attr().
                                Default False. WARNING: files are overwritten.
         simvecFilePrefix - Prefix of simulation outcome vector files, if
                            outputSimulatedVectors = True. The iteration
                            number and ".txt" is appened to form names like
                            "sim_outcome_1000.txt". Default "sim_outcome".
       Ainitial              - vector of 0/1 outcome variables to initialize
                               the outcome vector to before simulation process,
                               rather than starting from all 0 or random.
                               Default None, for random initialization here.
      bipartiteFixedMode - for bipartite networks only, the mode
                                 (MODE_A or MODE_B that is fixed to NA
                                 in simulation, for when outcome
                                 variable not defined for that mode,
                                 or None. Default None.

    The output is written to stdout in a format for reading by
    the R script plotSimulationDiagnostics.R.
    """
    assert(len(param_func_list) == len(labels))
    assert not (bipartiteFixedMode is not None and not bipartite)

    if directed:
        if bipartite:
            raise Exception("directed bipartite network not suppored")
        G = Digraph(arclist_filename, binattr_filename, contattr_filename,
                    catattr_filename, zone_filename)
    else:
        if bipartite:
            G = BipartiteGraph(arclist_filename, binattr_filename,
                               contattr_filename, catattr_filename,
                               zone_filename)
        else:
            G = Graph(arclist_filename, binattr_filename,
                      contattr_filename, catattr_filename, zone_filename)

    #G.printSummary()

    if degreestats:
        ##TODO directed and bipartite degrees
        degseq = np.array([G.degree(v) for v in G.nodeIterator()])
        labels += ['meanDegree1', 'varDegree1', 'meanDegree0', 'varDegree0']

    sys.stdout.write(' '.join(['t'] + labels + ['acceptance_rate']) + '\n')
    for (simvec,stats,acceptance_rate,t) in simulateALAAM(G, param_func_list,
                                                          theta,
                                                          numSamples,
                                                          iterationInStep,
                                                          burnIn,
                                                          sampler_func = sampler_func,
                                                          Ainitial = Ainitial,
                                                          bipartiteFixedMode = bipartiteFixedMode):
        if degreestats:
            ## mean and variance of degrees of nodes with outcome = 1
            meanDegree1 = np.mean(degseq[np.nonzero(simvec == 1)[0]])
            varDegree1 = np.var(degseq[np.nonzero(simvec == 1)[0]])
            ## mean and variance of degrees of nodes with outcome = 0
            meanDegree0 = np.mean(degseq[np.nonzero(simvec == 0)[0]])
            varDegree0 = np.var(degseq[np.nonzero(simvec == 0)[0]])
            stats = np.append(stats, [meanDegree1, varDegree1,
                                      meanDegree0, varDegree0])

        sys.stdout.write(' '.join([str(t)] + [str(x) for x in list(stats)] +
                                  [str(acceptance_rate)]) + '\n')
        if outputSimulatedVectors:
            outfilename = simvecFilePrefix + "_" + str(t) + os.path.extsep + "txt"
            with open(outfilename, 'w') as f:
                f.write("outcome\n")
                f.write("\n".join(["NA" if int(x) == NA_VALUE else str(int(x))
                                   for x in simvec]))
