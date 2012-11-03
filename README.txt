
===================
 icemac.songbeamer
===================

Library to read and write `SongBeamer`_ files.

.. contents::

Supported SongBeamer versions
=============================

Currently only version Songbeamer version 2 is supported. (Internal version
number in .sng files: ``#Version=3``.)

I do not have access to other SongBeamer versions so I do not know the file
structure there.

.. _`SongBeamer` : http://songbeamer.com

Supported Python version
========================

Runs on Python 3.2 and 3.3 is required. Older Python versions are not
supported.

Running Tests
=============

To run the tests call::

  $ python3.2 setup.py test -q

or (after having installed `nose`_ but with with coverage analysis)::

  $ nosetests

.. _`nose` : http://pypi.python.org/pypi/nose


Hacking
=======

Fork me on: https://bitbucket.org/icemac/icemac.songbeamer

.. image:: https://secure.travis-ci.org/icemac/icemac.songbeamer.png