cimport numpy as np
np.import_array()

# Include python cfunction
cdef extern from "accelerate.h":
  void Magnetization(long* conf, int L)
  void Energy(long* conf, int L)
  void MCSweeps(long* conf, int L, double T, int Nstep)

# Wrapper for our functions in C/C++
def c_Magnetization(np.ndarray[long, ndim=2, mode='c'] input not None, int L):
    """
    called by c_Magnetization(self.conf, L)
    """
    Magnetization(&input[0,0], input.shape[0]);

    return None

def c_Energy(np.ndarray[long, ndim=2, mode='c'] input not None, int L):
    Energy(&input[0,0], input.shape[0]);

    return None

def c_MCSweeps(np.ndarray[long, ndim=2, mode='c'] input not None, int L, int T, int Nstep):

    MCSweeps(&input[0,0], input.shape[0], T, Nstep);

    return None
