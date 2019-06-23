from distutils.core import setup, Extension
import numpy
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("accelerate_lib",
                             sources=["accelerate_module.pyx", "accelerate.c"],
                             include_dirs=[numpy.get_include()])],
)
