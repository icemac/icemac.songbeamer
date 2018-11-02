=========
 Changes
=========

1.0 (2018-11-02)
================

Backwards incompatible changes
------------------------------

- The ``icemac.songbeamer.SNG`` instances no longer store the data on the
  `data` attribute but it now behaves like a ``dict`` thus allowing direct dict
  access to the data.

- It is no longer possible to use attributes on ``icemac.songbeamer.SNG``
  instances to read and store encoded bytes data. Either read/write text data
  from/to the ``icemac.songbeamer.SNG`` instance using the `dict` API or use
  the ``parse`` function (see next item) to import resp. use ``.SNG.export()``
  to export the data encoded.

- Add a function ``icemac.songbeamer.parse()`` converting a byte stream
  into a ``icemac.songbeamer.SNG`` instance. It replaces the class method on
  the `SNG` instance. It returns ``None`` if the data cannot be
  parsed and it logs an error message.

- Drop support for Python 3.5, 3.6 and PyPy3, thus only supporting Python 3.7
  now.

Features
--------

- Add a function ``icemac.songbeamer.open()`` to open a file given by a path
  and get a ``icemac.songbeamer.SNG`` instance.

- Make ``.SNG.export()`` robust against missing text in songs.

- Add a command line script `songbeamer-xls-export` exporting titles and song
  book numbers from folder containing SongBeamer files to an XLS file. To be
  able to use it `icemac.songbeamer` has to be installed with the ``xls`` extra
  like this::

    $ pip install "icemac.songbeamer[xls]"

- Support UTF-8 encoded SongBeamer files starting with the UTF-8 BOM.

- Change license from ZPL to MIT.


0.3 (2018-10-07)
================

- Add support for Python 3.5 to 3.7 and PyPy3.

- Drop support for Python 3.2 and 3.3.


0.2.0 (2012-10-31)
==================

- Add ability to parse bytes objects.

- Sorting keys in export file to be compatible across Python 3.2 and 3.3.


0.1.0 (2012-05-05)
==================

- Initial public release.


