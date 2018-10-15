#!/usr/bin/env python
import re
from setuptools import setup, find_packages


def read_requirements(req_file):
    return [l for l in re.sub(r"\s*#.*\n", "\n", req_file.read()).splitlines() if l]


with open("requirements/base.txt") as f:
    REQUIREMENTS = read_requirements(f)

with open("requirements/test.txt") as f:
    TEST_REQUIREMENTS = read_requirements(f)

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
