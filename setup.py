from setuptools import setup, find_packages

from codecs import open
from os import path

with open(path.join('.', 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

name='iint-gui'
version='0'
release='0.3.6'

setup(
    name='iintgui',
    version='0.3.6',

    description='iintgui: ', 
    long_description=long_description,

    url='https://github.com/syncope/iintgui',

    author='Ch.Rosemann',
    author_email='christoph.rosemann@desy.de',
    
    license='GPLv2',
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='photon science data processing analysis gui interactive',
    
    packages=['iintgui',],
    
    package_dir = { 'iintgui':'iintgui',},
    include_package_data=True,

    scripts = ['iintgui/bin/iint-gui'],
)

