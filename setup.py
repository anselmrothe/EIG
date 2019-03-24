from distutils.spawn import find_executable
from distutils.core import setup
from distutils.command.clean import clean
from Cython.Build import cythonize
from setuptools import Extension, find_packages
import numpy
import os

CWD = os.getcwd()
BATTLESHIP_ROOT = os.path.join(CWD, "eig", "battleship")

class DeepClean(clean):
    def run(self):
        super().run()
        # clean .cpp/.so files
        clean_path = os.path.join(BATTLESHIP_ROOT, "cython")
        print("removing '{}/*.[so|cpp]'".format(clean_path))
        for f in os.listdir(clean_path):
            if f.endswith(".cpp") or f.endswith(".so"):
                os.remove(os.path.join(clean_path, f))


compile_args = {
    "include_dirs": [numpy.get_include(), os.path.join(BATTLESHIP_ROOT, "cpp")],
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

long_description = open("README.md").read()

setup(
    name="expected-information-gain",
    description="Parsing, executing, and calculating expected information gain for program-form questions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0.3",
    url='https://github.com/anselmrothe/EIG',
    license="MIT",
    packages=find_packages(exclude=("test",)),
    install_requires=["numpy", "cython"],
    include_package_data=True,
    test_suite="test",
    ext_modules=cythonize(extensions),
    cmdclass={'clean': DeepClean}
)
