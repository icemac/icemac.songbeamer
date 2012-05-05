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

Usage
=====

Importing a .sng file
---------------------

To import a .sng file call:

  >>> from icemac.songbeamer import SNG
  >>> sng = SNG.parse(open('my_song.sng', 'rb')
  >>> sng.data
  {'Text': 'La la la\n---\nLei lei lei',
   'Version': 3,
   'Author': 'me'}

To access the raw values imported from the .sng file access them using
getattr:

  >>> sng.Version
  b'3'
