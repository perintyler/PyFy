"""setup.py"""

import setuptools

from setuptools import setup

PACKAGE_NAME = 'object_validation'

with open('./requirements.txt') as f:
  requirements = f.read().splitlines()

setup(
  name=PACKAGE_NAME,
  package_dir={PACKAGE_NAME: './src'},
  install_requires=requirements
)

