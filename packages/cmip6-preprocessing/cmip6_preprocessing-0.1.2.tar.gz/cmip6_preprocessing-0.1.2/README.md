[![Anaconda Cloud](https://anaconda.org/conda-forge/cmip6_preprocessing/badges/version.svg)](https://anaconda.org/conda-forge/cmip6_preprocessing)
[![Pypi](https://img.shields.io/pypi/v/cmip6_preprocessing.svg)](https://pypi.org/project/cmip6_preprocessing)
[![Build Status](https://travis-ci.com/jbusecke/cmip6_preprocessing.svg?branch=master)](https://travis-ci.com/jbusecke/cmip6_preprocessing)
[![codecov](https://codecov.io/gh/jbusecke/cmip6_preprocessing/branch/master/graph/badge.svg)](https://codecov.io/gh/jbusecke/cmip6_preprocessing)
[![License:MIT](https://img.shields.io/badge/License-MIT-lightgray.svg?style=flt-square)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/215606850.svg)](https://zenodo.org/badge/latestdoi/215606850)

# cmip6_preprocessing

Frustrated with how 'dirty' CMIP6 data still is? Do you just want to run a simple (or complicated) analysis on various models and end up having to write logic for each seperate case? Then this package is for you.

Developed during the [cmip6-hackathon](https://cmip6hack.github.io/#/) this package provides utility functions that play nicely with [intake-esm](https://github.com/NCAR/intake-esm).

We currently support the following functions

1. Fix inconsistent naming of dimensions and coordinates
2. Fix inconsistent values,shape and dataset location of coordinates
3. Homogenize longitude conventions
4. Fix inconsistent units

The following issues are under development:
1. Reconstruct/find grid metrics
2. Arrange different variables on their respective staggered grid, so they can work seamlessly with [xgcm](https://xgcm.readthedocs.io/en/latest/)

Please check out the [tutorial](notebooks/tutorial.ipynb) for some examples using the [pangeo cloud](ocean.pangeo.io).

## Installation

Install `cmip6_preprocessing` via pip:

`pip install cmip6_preprocessing`

or conda:

`conda install -c conda-forge cmip6_preprocessing`

