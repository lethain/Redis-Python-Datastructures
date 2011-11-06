#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(name='redis_ds',
      version='1.0',
      description='simple python datastructure wrappings for redis',
      author='Will Larson',
      author_email='lethain@gmail.com',
      url='http://github.com/lethain/Redis-Python-Datastructures',
      packages=['redis_ds'],
      package_dir={'redis_ds': 'src/Redis-Python-Datastructures'},
      include_package_data=True,
      requires=(
        'redis'
        )
     )
