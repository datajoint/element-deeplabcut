#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path


pkg_name = 'workflow_behavior'
here = path.abspath(path.dirname(__file__))

long_description = """"
# Workflow for monitoring DeepLabCut post estimaton

+ [element-lab](https://github.com/datajoint/element-lab)
+ [element-animal](https://github.com/datajoint/element-animal)
+ [element-session](https://github.com/datajoint/element-session)
+ [element-behavior](https://github.com/datajoint/element-behavior)
"""

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(path.join(here, pkg_name, 'version.py')) as f:
    exec(f.read())

setup(
    name='workflow-behavior',
    version=__version__,
    description="DataJoint Elements for DeepLabCut pose estimation",
    long_description=long_description,
    author='DataJoint',
    author_email='info@DataJoint.com',
    license='MIT',
    url='https://github.com/datajoint/workflow-behavior',
    keywords='neuroscience behavior deeplabcut datajoint',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=requirements,
)
