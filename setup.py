#!/usr/bin/env python
import re
from setuptools import setup, find_packages


def read_requirements(req_file):
    return [
        line for line in re.sub(r"\s*#.*\n", "\n", req_file.read()).splitlines() if line
    ]


with open("requirements/base.txt") as f:
    REQUIREMENTS = read_requirements(f)

with open("requirements/test.txt") as f:
    TEST_REQUIREMENTS = read_requirements(f)

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="naovoce",
    version="2.0.0a",
    description="Na-ovoce.cz site backend",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/jsmesami/naovoce",
    author="Ondřej Nejedlý",
    author_email="software@na-ovoce.cz",
    license="MIT License",
    packages=find_packages(),
    entry_points={"console_scripts": ["naovoce=naovoce.manage:main"]},
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
        "License :: OSI Approved :: MIT License"
        "Programming Language :: Python :: 3.8",
    ],
)
