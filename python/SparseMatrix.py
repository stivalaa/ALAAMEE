#
# File:    SparseMatrix.py
# Author:  Alex Stivala
# Created: August 2022
#
# Defines a sparse matrix data structure
#


class SparseMatrix:
    """The sparse matrix is represented as a dictionary of
    dictionaries.  Indexed by integers 0..n-1. The outermost
    dictionary has the row i as a key, and dictionary as value.  Then
    this dictionary has the nonzero columns j for row i as the keys,
    and the nonzero (i,j) value as value.

    So A[i] is a dictionary with k entries, where k is number of nonzero
    entries in row i.

    To make these operations simple (no special cases for all zero
    rows, it graph is initialized so that A[i] = dict() for all 0 <= i < n:
    dict(zip(range(n), [dict() for i in range(n)]))

    Note this is very similar to the Graph or Digraph data structures,
    which are effectively sparse adjacency matrix (adjacency list)
    storage, with operations specific to graphs.

    An alternative would be something like compressed sparse row (CSR)
    storage, using 3 arrays, but dictionaries are very convenient in
    Python (and arrays are not).

    """

    def __init__(self, n):
        """
        Construct sparse square matrix with n rows, all zero.

        Parameters:
            n                  - number of rows

        """
        self.A = None  # dict of dicts as described above

        # empty sparse matrix n rows        
        self.A = dict(list(zip(list(range(n)), [dict() for i in range(n)])))


    def numRows(self):
        """
        Return number of rows in matrix
        """
        return len(self.A)
    
    def numNonZero(self):
        """
        Return number of nonzero entries in matrix
        """
        return sum([len(list(v.keys())) for v in self.A.values()])
    
    def numNonZeroInRow(self, i):
        """
        Return number of nonzero entries in row i
        """
        return len(self.A[i])

    def rowNonZeroValuesIterator(self, i):
        """
        Return iterator over nonzero entries in row i
        """
        return iter(self.A[i].keys())

    def insertValue(self, i, j, v):
        """
        Insert value v for A(i,j) in place
        """
        self.A[i][j] = v

    def removeValue(self, i, j):
        """
        Remove value for A(i,j) in place
        """
        self.A[i].pop(j)

