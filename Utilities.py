# Module for argument collection, data analysis and more

import sys
import numpy as np
import matplotlib.pyplot as plt
from Ising import Ising
from scipy.stats import moment

def get_arguments():

    if (len(sys.argv) > 5) or (len(sys.argv) < 3):
        print("Wrong number of arguments, give two (and -a for acceleration), e.g.:")
        print("Main.py 100 300 -1 -a") # L, T, J, acceleration parameter
        raise Exception('Wrong arguments')

    cpp = True if ('-a' in sys.argv) else False

    L = int(sys.argv[1])
    T = float(sys.argv[2])

    return L, T, cpp

def PBC(L):
    na = np.arange(0,int(L),1)+1
    na[-1] = 0

    nm = np.arange(0,int(L),1)-1
    nm[0] = int(L)-1

    return na, nm

def autocorrelation():
    pass

def errorbar(values, order):
    pass

def susceptibility(magn, L, T):
    M_2 = moment(magn, 2)
    susc = M_2/(L**2*T)
    #error = errorbar(magn)
    return susc

def heat_capacity(energy, L, T):
    E_2 = moment(energy, 2)
    E_0 = moment(energy, 1)
    C = (E_2 - E_0)/(L**2 * T**2)
    return C
