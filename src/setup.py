from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

setup(
	cmdclass = {'build_ext':build_ext},
	ext_modules = [Extension("lattice_SAW",
							  sources = ["lattice_SAW.pyx","c_lattice_SAW.cpp"],
							  extra_compile_args=['-std=c++11','-stdlib=libc++'],
							  language="c++",
							  include_dirs = [numpy.get_include()])],
)
