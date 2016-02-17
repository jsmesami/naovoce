#!/usr/bin/env python

from setuptools import setup, find_packages

# TODO: This needs more love.

setup(
    name='naovoce',
    version='1.0a',
    url='https://github.com/jsmesami/naovoce.git',
    author='Ondra Nejedlý',
    license='MIT',
    packages=find_packages(),
    scripts=[
        'src/manage.py'
    ],
)
