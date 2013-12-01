#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
import redis_ds

setup(name='redis_ds',
      version=redis_ds.__version__,
      description='simple python datastructure wrappings for redis',
      author='Will Larson',
      author_email='lethain@gmail.com',
      url='http://github.com/lethain/Redis-Python-Datastructures',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
     )
