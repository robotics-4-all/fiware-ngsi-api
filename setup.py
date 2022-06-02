#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='fiware-ngsi-api',
      version='0.1.0',
      description='Python API client to communicate with Orion Context Broker',
      url='',
      author='Evripidis Chondromatidis',
      author_email='eurichon1996@gmail.com',
      license='Apache v2',
      packages=find_packages(),
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False
      )
