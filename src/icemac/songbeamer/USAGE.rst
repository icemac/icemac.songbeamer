=======
 Usage
=======

Importing a .sng file
=====================

To import a `.sng` file use the ``open`` function in the module
``icemac.songbeamer``. It expects a filename and path and returns a SNG
instance:

  >>> import icemac.songbeamer
  >>> import pkg_resources
  >>> filename = pkg_resources.resource_filename(
  ...     'icemac.songbeamer.tests', 'example.sng')
  >>> sng = icemac.songbeamer.open(filename)
  >>> sng.__class__
  <class 'icemac.songbeamer.sng.SNG'>

Alternatively there is a function ``parse`` in the same module which parses
bytes (e. g. read from a binary file) into an SNG instance:

  >>> with open(filename, 'rb') as file:
  ...     sng = icemac.songbeamer.parse(file.read())
  >>> sng.__class__
  <class 'icemac.songbeamer.sng.SNG'>

Accessing a file's data
=======================

The SNG instance extends ``dict`` so the date is accessible via the usual
python ``dict`` API:

  >>> from pprint import pprint
  >>> pprint(sng)
  {'Author': 'me',
   'Text': ['La la la', '---', 'Lei lei lei'],
   'Version': 3}
  >>> sng['Title'] = 'Mÿ šôñg'

The values are stored as numbers resp. strings (text):

  >>> sng['Version']
  3
  >>> sng['Author']
  'me'

Exporting a .sng file
=====================

  >>> from tempfile import TemporaryFile

To export to a .sng file use the ``export`` method. It expects a byte stream
(io.BytesIO or open binary file) as argument to write into:

  >>> with TemporaryFile() as file:
  ...     sng.export(file)
  ...     _ = file.seek(0)
  ...     pprint(file.readlines())
  [b'#Author=me\r\n',
   b'#Title=M\xff \x9a\xf4\xf1g\r\n',
   b'#Version=3\r\n',
   b'---\r\n',
   b'La la la\r\n',
   b'---\r\n',
   b'Lei lei lei']
