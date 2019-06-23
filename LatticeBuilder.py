import numpy as np
import random

def LatticeBuilder(L, type):
    if (type == 's'): #square
        grid = 2*np.random.randint(2,size=(L,L)) - 1
    return grid
