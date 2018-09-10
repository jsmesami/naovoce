#!/usr/bin/env python

from setuptools import setup, find_packages

with open("requirements/base.txt") as f:
    REQUIREMENTS = f.read().splitlines()

with open("requirements/test.txt") as f:
    TEST_REQUIREMENTS = f.read().splitlines()

setup(
    name="naovoce",
    version="2.0.0a",
    url="https://github.com/jsmesami/naovoce.git",
    author="Ondřej Nejedlý",
    author_email="software@na-ovoce.cz",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    description="Na-ovoce.cz site backend",
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    scripts=[
        'src/manage.py'
    ],
)
