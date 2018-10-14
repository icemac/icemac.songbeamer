=========
 Changes
=========

0.4 (unreleased)
================

- Drop support for Python 3.5, 3.6 and PyPy3, thus only supporting Python 3.7
  now.

- Add class method ``.SNG.open()`` to open a file given by a path.


- Class method ``.SNG.parse()`` now returns ``None`` if the file cannot be
  parsed and is logging an error message.

- Make ``.SNG.export()`` robust against missing Text in songs.


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


