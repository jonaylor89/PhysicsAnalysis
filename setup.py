
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="Physics Analysis",
    ext_modules=cythonize(["*.pyx"])
)
