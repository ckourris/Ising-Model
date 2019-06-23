# SQIsing.py: Simulation of 2D Ising Model
# Ising Class

import numpy as np
import math as m
import random
import matplotlib.pyplot as plt
from LatticeBuilder import *
import Utilities
import accelerate_lib

class Ising(object):

    def __init__(self, L, grid, T, cpp):
        self.conf = LatticeBuilder(int(L), grid)
        self.T = T
        self.L = L
        self.cpp_enabled = cpp

        # PBC Fixing: These arrays have the properties
        # np(i) = i+1 , np(L-1) = 0
        # nm(i) = i-1 , nm(0) = L-1
        self.np, self.nm  = Utilities.PBC(L)

    def Energy(self):
        # Returns total energy of configuration
        # Summation over all i, j and then divide by 2 to account for double sum
        E = 0
        for i in range(self.L):
            for j in range(self.L):
                E = E + self.Energy_NN(i, j)
        return E/2

    def Energy_NN(self, x, y):
        # Calculates the interaction energy of the spin at site x,y
        # with its 4 nearest neighbours, respecting PBC
        dE = self.conf[x][y]*(self.conf[self.nm[x]][y] + self.conf[self.np[x]][y] \
             + self.conf[x][self.nm[y]] + self.conf[x][self.np[y]])

        return dE

    def Magnetization(self):
        return np.sum(self.conf)

    def MCSweeps(self, Nmcs):
        # Performs 1 Monte Carlo Sweep

        dEs = np.arange(-8,12,4)
        exp = [np.exp(E/self.T) for E in dEs]

        for i in range(Nmcs):
            for j in range(self.L*self.L):
                x, y =  np.random.randint(self.L,size=2)

                Enn = -1.0*self.Energy_NN(x,y)
                #dE = E_flipped - E_notflipped, easier dE = -2*E_notflipped
                dE = -2*Enn

                # Need exp(-dE/T)
                index = np.where(dEs == -dE)[0][0]

                Pflip = np.minimum(1,exp[index])
                r = random.uniform(0,1)

                # We accept if Pflip > r
                if Pflip > r:
                    self.conf[x][y] = -1*self.conf[x][y]

        return None

    def Simulate(self, NStep, NWarmup, Nmeas):
        # Monte Carlo algorithm, performs Nmcs MC Sweeps
        # To avoid correlation of consecutive configurations we define a
        # sweep as LxL attempts to flip a spin.

        # First warm up for Nwarmup steps/No visualization during those
        self.MCSweeps(NWarmup)

        if self.cpp_enabled:
            accelerate_lib.c_MCSweeps(self.conf,self.L, self.T, NWarmup)
        else:
            self.MCSweeps(NWarmup)

        # Begin simulation including measurements and visualization

        plt.ion()
        plt.show()
        im = plt.imshow(self.conf, cmap='gray', vmin=-1, vmax=1, interpolation='none')

        magnetization, energy = [], []
        for i in range(Nmeas):

            if self.cpp_enabled:
                accelerate_lib.c_MCSweeps(self.conf,self.L, self.T, NStep)
                M = accelerate_lib.c_Magnetization(self.conf, self.L)
                E = accelerate_lib.c_Energy(self.conf, self.L)
            else:
                self.MCSweeps(NStep)
                M = self.Magnetization()
                E = self.Energy()

            magnetization.append(M)
            energy.append(E)
            #To Do: Entropy
        """
            im.set_data(self.conf)
            plt.draw()
            plt.pause(.01)

        plt.ioff()
        plt.close()
        """
        return np.array(magnetization), np.array(energy)
