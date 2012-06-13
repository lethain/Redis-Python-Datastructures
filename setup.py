import os
import sys

from setuptools import Command, setup, find_packages
__version__ = (0, 0, 1)

setup(
    name = 'rpd',
    version = '.'.join([str(x) for x in __version__]),
    packages = find_packages(),
    author = 'lethain',
    author_email = '',
    url = '',
    description = 'redis python datastructures',
    install_requires = ['redis'],
)
