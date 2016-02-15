#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='naovoce',
    version='0.9',
    author='Ondra Nejedlý',
    packages=find_packages(),
    scripts=[
        'src/manage.py'
    ],
)
