#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='javaobject',
      version='0.1',
      description='java object serialization library',
      author='Lo Lynx',
      author_email='lodevil@live.cn',
      url='https://github.com/lodevil/javaobject',
      packages=['javaobject', 'javaobject.java', 'javaobject.java.javabuiltins'],
      )
