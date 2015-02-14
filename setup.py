#!/usr/bin/env python

import os

from setuptools import setup, find_packages

README = None
with open(os.path.abspath('README.md')) as fh:
  README = fh.read()

setup(
  name='bio',
  version='0.0.2',
  description=README,
  author='Stephen Holsapple',
  author_email='sholsapp@gmail.com',
  url='http://www.google.com',
  install_requires=[
    'argparse',
  ],
  test_requires=[
    'pytest',
  ],
  entry_points = {
    'console_scripts': [
      'global-align = bio.bin.global:main',
      'local-align = bio.bin.local:main',
    ],
  },
  packages=find_packages(),
)
