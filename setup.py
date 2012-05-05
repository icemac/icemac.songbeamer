# -*- coding: utf-8 -*-
# Copyright (c) 2012 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools
import sys


def read(path):
    return open(os.path.join(*path.split('/'))).read()


version = '0.1.0'


setuptools.setup(
    name='icemac.songbeamer',
    version=version,
    description=(
        "Python 3 library to import from and export to SongBeamer format."),
    long_description="\n\n".join([
        read('README.txt'),
        read('CHANGES.txt'),
        read('TODO.txt'),
        read('src/icemac/songbeamer/USAGE.txt'),
        ]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Buildout',
        'Framework :: Buildout :: Recipe',
        'Intended Audience :: Developers',
        'Intended Audience :: Religion',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Religion',
        ],
    keywords=(
        'python 3 songbeamer import export'),
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    url='http://pypi.python.org/icemac.songbeamer',
    license='ZPL 2.1',
    packages=setuptools.find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['icemac'],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'nose>=1.0',
        'coverage',
        ],
    install_requires=[
        'setuptools',
        ],
    tests_require=[],
    test_suite="icemac.songbeamer.tests",
    entry_points="""
      [console_scripts]
      sng2sng = icemac.songbeamer.sng:sng2sng
      """,
    )
