###
# Installs the iopenscad module and then the kernel description
#

import pathlib, os, distutils.core, setuptools 
from setuptools import setup
from setuptools.command import easy_install
from setuptools.command.install import install
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig
import pkg_resources


# # don't invoke the original build_ext for this special extension
# class CMakeExtension(Extension):
#     def __init__(self, name):
#         super().__init__(name, sources=[])

# # Extended install which also installs the kernel
# class build_ext(build_ext_orig):
#     def run(self):
#         self.installKernel()

#     def installKernel(self):
#         kernel = pkg_resources.resource_filename("iopenscad","kernel.json")
#         if not os.path.exists(kernel):
#             raise Exception('The kernel does not exist {}'.format(kernel))

#         directory = str(pathlib.Path(kernel).parent)
#         if not os.path.isdir(directory):
#             raise Exception('The directory does not exist {}'.format(directory))

#         cmd = 'jupyter kernelspec install ' + directory
#         if os.system(cmd) != 0:
#             raise Exception('Could not install kernelspec {}'.format(cmd))


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pschatzmann-test-001",
    version="1.0.9",
    description="Jupyter kernel for OpenSCAD",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pschatzmann/openscad-kernel",
    author="Phil Schatzmann",
    author_email="phil.schatzmann@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
#    ext_modules=[CMakeExtension('foo/foo')],
    packages=["iopenscad"],
    include_package_data=True,
#    install_requires=["jupyter"],
#    cmdclass={'build_ext': build_ext}

)



