
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

Runs on Python 3.5 up to 3.7 and PyPy3. Older Python versions are not
supported.

Running Tests
=============

To run the tests call::

  $ tox

(You maybe have to install `tox` beforehand using: ``pip install tox``.)

Hacking
=======

Fork me on: https://bitbucket.org/icemac/icemac.songbeamer

.. image:: https://secure.travis-ci.org/icemac/icemac.songbeamer.png
   :target: https://travis-ci.org/icemac/icemac.songbeamer.png
