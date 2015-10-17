# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import sys

if sys.version_info < (3,5,0):
    sys.exit('It requires Python version 3.5.0 or higher.')

here = path.abspath(path.dirname(__file__))

setup(
    name='logger',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0',
    description='A simple logger with attachable handlers',
    long_description='',
    url='https://github.com/lablup/logger',
    author='Lablup Inc.',
    author_email='joongi@lablup.com',
    license='Apache 2.0',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['simplejson', 'toml', 'umsgpack'],
    extras_require={
        'dev': [],
        'test': [],
    },
    data_files=[],

    entry_points={
        'console_scripts': ['run-logger=logger:main'],
    },
)
