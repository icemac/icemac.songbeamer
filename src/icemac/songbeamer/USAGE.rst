=======
 Usage
=======

Importing a .sng file
=====================

To import a .sng file use the ``parse`` class method. It expects a byte
stream (io.BytesIO or open file) or a bytes object as argument to read from:

  >>> from icemac.songbeamer import SNG
  >>> with open('example.sng', 'rb') as file:
  ...     sng = SNG.parse(file)

  >>> with open('example.sng', 'rb') as file:
  ...     sng = SNG.parse(file.read())


Accessing a file's data
=======================

The parsed data is stored in the ``data`` attribute of the object:

  >>> from pprint import pprint
  >>> pprint(sng.data)
  {'Author': 'me',
   'Text': ['La la la', '---', 'Lei lei lei'],
   'Version': 3}

To access the raw values imported from the .sng file get them using `getattr`:

  >>> sng.Version
  b'3'

Exporting a .sng file
=====================

  >>> from tempfile import TemporaryFile

To export to a .sng file use the ``export`` method. It expects a byte stream (io.BytesIO or open file) as argument to write into:

  >>> with TemporaryFile() as file:
  ...     sng.export(file)
  ...     _ = file.seek(0)
  ...     pprint(file.readlines())
  [b'#Author=me\r\n',
   b'#Version=3\r\n',
   b'---\r\n',
   b'La la la\r\n',
   b'---\r\n',
   b'Lei lei lei']


