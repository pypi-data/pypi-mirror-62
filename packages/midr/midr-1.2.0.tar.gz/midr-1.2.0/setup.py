#!/usr/bin/env python3
# -*-coding:Utf-8 -*

import setuptools
from Cython.Build import cythonize
import numpy as np

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="midr",
    version="1.2.0",
    packages=['midr'],
    install_requires=[
        'scipy>=1.3',
        'numpy>=1.16',
        'pynverse>=0.1',
        'pandas>=0.25.0',
        'matplotlib>=3.1.0',
        'mpmath>=1.1.0',
        'cython>=0.28.0'
    ],
    author="Laurent Modolo",
    author_email="laurent.modolo@ens-lyon.fr",
    description="Compute idr from m NarrowPeak files and a merged NarrowPeak",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitbio.ens-lyon.fr/LBMC/sbdm/midr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, \
version 2.1 (CeCILL-2.1)",
        "Operating System :: OS Independent"
    ],
    test_suite='pytest',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['midr=midr.__main__:main'],
    },
    ext_modules=cythonize(
        "midr/c_archimedean.pyx",
        language_level=3
    ),
    include_dirs=[np.get_include()],
    build_ext='build_ext'
)
