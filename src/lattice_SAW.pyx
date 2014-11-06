import cython
import numpy as np
cimport numpy as np

cdef extern from "c_lattice_SAW.h":
	void c_lattice_SAW(double* chain, int N, double l0, int ve)

@cython.boundscheck(False)
@cython.wraparound(False)

def lattice_SAW(int N, double l0, int ve):
	cdef np.ndarray[double,ndim = 1,mode="c"] chain = np.zeros(N*3)
	c_lattice_SAW(&chain[0],N,l0,ve)
	return chain