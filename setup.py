from distutils.core import setup
from Cython.Build import cythonize
from setuptools import Extension
import numpy

extensions = [
    Extension("eig.battleship.question.executor", 
            ["eig/battleship/question/executor.pyx"],
            include_dirs=[numpy.get_include()],
            extra_compile_args=["-std=c++11", "-stdlib=libc++"],
            extra_link_args=["-std=c++11"])]

setup(
    test_suite="test",
    ext_modules=cythonize(extensions)
)