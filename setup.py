#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

pkg_name = "workflow_deeplabcut"
here = path.abspath(path.dirname(__file__))

long_description = """"
# Workflow for monitoring DeepLabCut pose estimaton

+ [element-lab](https://github.com/datajoint/element-lab)
+ [element-animal](https://github.com/datajoint/element-animal)
+ [element-session](https://github.com/datajoint/element-session)
+ [element-deeplabcut](https://github.com/datajoint/element-deeplabcut)
"""

with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read().splitlines()

with open(path.join(here, pkg_name, "version.py")) as f:
    __version__ = "0.0.0"  # overwritten. set to pass linter
    exec(f.read())

setup(
    name="workflow-deeplabcut",
    version=__version__,
    description="DataJoint Elements for DeepLabCut pose estimation",
    long_description=long_description,
    author="DataJoint",
    author_email="info@DataJoint.com",
    license="MIT",
    url="https://github.com/datajoint/workflow-deeplabcut",
    keywords="neuroscience deeplabcut deeplabcut datajoint",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=requirements,
)
