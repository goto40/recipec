#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
from setuptools import setup, find_packages

NAME = 'recipec'
DESC = 'recipe language: compiler and validator'
VERSION = '0.0'
AUTHOR = 'Pierre Bayerl'
AUTHOR_EMAIL = 'pierre DOT bayerl AT googlemail DOT com'
LICENSE = 'MIT'
URL = 'https://github.com/goto40/recipec'
DOWNLOAD_URL = 'https://github.com/goto40/recipec/archive/v{0}.tar.gz'.format(VERSION)
README = codecs.open(os.path.join(os.path.dirname(__file__), 'README.rst'),
                     'r', encoding='utf-8').read()

if sys.argv[-1].startswith('publish'):
    if os.system('pip list | grep wheel'):
        print('wheel not installed.\nUse `pip install wheel`.\nExiting.')
        sys.exit()
    if os.system('pip list | grep twine'):
        print('twine not installed.\nUse `pip install twine`.\nExiting.')
        sys.exit()
    os.system('python setup.py sdist bdist_wheel')
    if sys.argv[-1] == 'publishtest':
        os.system('twine upload -r test dist/*')
    else:
        os.system('twine upload dist/*')
        print('You probably want to also tag the version now:')
        print('  git tag -a {0} -m "version {0}"'.format(VERSION))
        print('  git push --tags')
    sys.exit()

my_packages = find_packages(exclude=['tests.*', 'tests'])
print('packages = {}'.format(my_packages))

setup(
    name=NAME,
    version=VERSION,
    description=DESC,
    long_description=README,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=my_packages,
    package_data={'': ['*.tx', '*.template']},
    install_requires=['textX', 'jinja2', 'pytest'],
    keywords='idl',
    entry_points={
        'console_scripts': [
            'recipec = recipec.console:recipec',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]

)
