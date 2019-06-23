import numpy as np
from Utilities import *
from Ising import Ising
import accelerate_lib
import matplotlib.pyplot as plt

def main():
    L, T, cpp = get_arguments()

    # For Grid write 's' for square
    # Initialization of grid
    #system = Ising(L, 's', T, cpp)

    # Nsteps: the number of MCS between measurement of observables
    # Nmeas: the total number of measurements to be performed
    # NWarmup: the number of warm up sweeps to reach equiilbrium

    NStep = 1
    NWarmup = 0
    Nmeas = 10

    susc = []
    C = []
    temp = []
    T = 2.0
    while T <= 2.5:
        print("T = ", T, "with cpp = ", cpp)
        system = Ising(L,'s', T, cpp)
        magnetization, energy = system.Simulate(NStep, NWarmup, Nmeas)

        susc.append(susceptibility(magnetization, L, T))
        C.append(heat_capacity(energy, L, T))
        temp.append(T)

        T = T + 0.01

    plt.plot(temp, susc, 'ro')
    plt.title("Susceptibility versus temperature")
    plt.show()

    plt.plot(temp, C, 'ro')
    plt.title("Heat capacity versus temperature")
    plt.show()

    #magnetization, energy = system.Simulate(NStep, NWarmup, Nmeas)

if __name__ == '__main__':
    main()
