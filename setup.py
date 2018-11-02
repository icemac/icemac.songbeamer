# -*- coding: utf-8 -*-
# Copyright (c) 2012,2018 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools


def read(path):
    return open(os.path.join(*path.split('/'))).read()


version = '1.0'


setuptools.setup(
    name='icemac.songbeamer',
    version=version,
    description=(
        "Python 3 library to import from and export to SongBeamer format."),
    long_description="\n\n".join([
        read('README.rst'),
        read('CHANGES.rst'),
        read('TODO.rst'),
        read('src/icemac/songbeamer/USAGE.rst'),
    ]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Religion',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Religion',
    ],
    keywords=(
        'python 3 songbeamer import export'),
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    url='https://github.com/icemac/icemac.songbeamer',
    license='MIT',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['icemac'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    extras_require=dict(
        test=[
            'pytest',
            'xlrd',
        ],
        xls=['xlwt'],
    ),
    entry_points="""
      [console_scripts]
      sng2sng=icemac.songbeamer.sng:sng2sng
      songbeamer-xls-export=icemac.songbeamer.xls:main
      """,
)
