#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

DIR = path.abspath(path.dirname(__file__))

with open(path.join(DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bigchaindb-abci',
    version='1.0.5',
    description='Python based ABCI Server for Tendermint',
    long_description=long_description,
    url='https://github.com/ipdb/bigchaindb-abci',
    author='Dave Bryson',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='blockchain tendermint abci',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "protobuf==3.6.1",
        "gevent==20.6.2",
        "colorlog==4.1.0",
    ],
    tests_require=[
        "pytest==5.3.5",
        "pytest-pythonpath==0.7.3",
        "pytest-cov==2.8.1"
    ],
    python_requires='>=3.6',
)
