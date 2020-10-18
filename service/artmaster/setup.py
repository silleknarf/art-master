#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='artmaster',
    version='0.1.0',
    description='Service backend for the craicbox game',
    author='Frank Ellis',
    author_email='silleknarf@gmail.com',
    url='https://github.com/silleknarf/art-master',
    packages=find_packages(exclude=('tests', 'docs'))
)