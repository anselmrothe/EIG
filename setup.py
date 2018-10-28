from distutils.core import setup
from Cython.Build import cythonize
from setuptools import Extension
import numpy
import os
from distutils.spawn import find_executable

cwd = os.getcwd()
compile_args = {
    "include_dirs": [numpy.get_include(), cwd + "/eig/battleship/cpp"],
    "extra_compile_args": ["-std=c++11"],
    "extra_link_args": ["-std=c++11"]
}

clang_executable = find_executable('clang++')
if clang_executable is None:
    os.environ["CC"] = "g++"
    os.environ["CXX"] = "g++"
else:
    os.environ["CC"] = "clang++"
    os.environ["CXX"] = "clang++"
    compile_args["extra_compile_args"].append("-stdlib=libc++")
    compile_args["extra_link_args"].append("-stdlib=libc++")

extensions = [
    Extension("eig.battleship.cython.executor",
            ["eig/battleship/cython/executor.pyx"],
            **compile_args
            ),
    Extension('eig.battleship.cython.hypothesis',
            ["eig/battleship/cython/hypothesis.pyx"],
            **compile_args)
]

setup(
    test_suite="test",
    ext_modules=cythonize(extensions)
)
