
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

At least Python 3.2 is required.

Running Tests
=============

To run the tests call::

  $ python3.2 setup.py test -q

or (with coverage analysis)::

  $ python3.2 setup.py nosetests


