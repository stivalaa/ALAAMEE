#
# File:    utils.py
# Author:  Alex Stivala
# Created: Feburary 2022
#
# Utility functions
#


# NA values for categorical and binary attributes (continuous uses float("nan"))
NA_VALUE = -1

def int_or_na(s):
    """
    Convert string to integer or NA value for "NA" for missing data
    
    Parameters:
       s  - string representation of integer or "NA" 

    Return value:
      integer value of s or NA_VALUE
    """
    return NA_VALUE if s == "NA" else int(s)


def float_or_na(s):
    """
    Convert string to float or NaN for "NA" for missing data
    
    Parameters:
       s  - string representation of integer or "NA"

    Return value:
      integer value of s or NA_VALUE
    """
    return float("NaN") if s == "NA" else float(s)

