from . import ENCODING
from base64 import b64encode, b64decode
from pathlib import Path
import dataclasses
import logging
import re
import typing


__all__ = ['open', 'parse', 'SNG', 'sng2sng']


log = logging.getLogger(__name__)
_open = open
HEADLINE_RE = re.compile(b'^#(.*?)=(.*)$')


def open(path):
    """Open a .sng file and return a SNG instance."""
    with _open(path, 'rb') as f:
        data = f.read()
    return parse(data, filename=path)


def parse(data, filename='<bytes>'):
    """Parse bytes into a SNG instance, return `None` if data is not valid."""
    if data.startswith(b'\xef\xbb\xbf'):
        encoding = 'utf-8'
        data = data[3:]
    else:
        encoding = ENCODING
    importer = _Importer(encoding=encoding)
    return importer.read(data, filename)


@dataclasses.dataclass(repr=False, eq=False, frozen=True)
class SNG(dict):
    """Dict describing a .sng file."""

    filename: str = '<bytes>'

    def export(self, byte_stream):
        """Export .sng file contents to a byte_stream."""
        exporter = _Exporter(ENCODING, byte_stream, self)
        return exporter.export()


@dataclasses.dataclass
class _Importer:
    """Import data from a .sng file to an SNG instance."""

    encoding: str = ENCODING

    _converters = {
        'Text': lambda x, encoding: x.decode(encoding).splitlines(),
        'Version': lambda x, encoding: int(x),
        'LangCount': lambda x, encoding: int(x),
        'Comments': lambda x, encoding: b64decode(x).decode(encoding),
        'Categories': lambda x, encoding: [
            y.decode(encoding) for y in x.split(b', ')],
        'Chords': lambda x, encoding: [
            y.split(',')
            for y in b64decode(x).decode(encoding).splitlines()],
    }

    def read(self, data, filename):
        """Import into a SNG instance, return `None` if data is not valid."""
        try:
            head, text = data.split(b'---', 1)
        except ValueError:
            log.error(
                '%r cannot be parsed: it does not contain `---`.', filename)
            return None
        sng = SNG(filename=Path(filename).name)
        sng['Text'] = self._import('Text', text.strip())
        try:
            sng.update(self._parse_head(head.splitlines()))
        except ValueError as e:
            log.error('%r cannot be parsed: %s', filename, e)
            return None
        return sng

    def _default_import(self, value, encoding=None):
        if encoding is None:
            encoding = self.encoding
        return value.decode(encoding)

    def _parse_head(self, lines):
        data = {}
        for lineno, line in enumerate(lines, 1):
            parsed_line = HEADLINE_RE.search(line)
            try:
                key, value = parsed_line.groups()
            except AttributeError:
                raise ValueError(
                    f'Invalid data structure in line {lineno}: {line!r}')
            key = self._default_import(key)
            data[key] = self._import(key, value)
        return data

    def _import(self, key, value):
        converter = self._converters.get(key, self._default_import)
        return converter(value, self.encoding)


@dataclasses.dataclass
class _Exporter:
    """Export an SNG instance to .sng file contents."""

    encoding: str
    stream: typing.BinaryIO
    data: SNG

    def export(self):
        for key in sorted(self.data):
            if key == 'Text':
                # Text needs to be the last line
                continue
            value = self.data[key]
            self.stream.write(
                b'#%(key)s=%(value)s\r\n' % {
                    b'key': self._default_export(key),
                    b'value': self._export(key, value)
                    })
        self.stream.write(b'---\r\n')
        if 'Text' in self.data:
            self.stream.write(self._export('Text', self.data['Text']))

    def _int_to_bytes(x, encoding):
        return bytes(str(x), encoding)

    def _chords_converter(x, encoding):
        chords = [','.join(y) for y in x]
        return b64encode(('\r'.join(chords)).encode(encoding) + b'\r')

    def _categories_converter(x, encoding):
        return b', '.join([y.encode(encoding) for y in x])

    _converters = {
        'Text': lambda x, encoding: ('\r\n'.join(x)).encode(encoding),
        'Version': _int_to_bytes,
        'LangCount': _int_to_bytes,
        'Comments': lambda x, encoding: b64encode(x.encode(encoding)),
        'Categories': _categories_converter,
        'Chords': _chords_converter,
    }

    def _default_export(self, value, encoding=None):
        if encoding is None:
            encoding = self.encoding
        return value.encode(encoding)

    def _export(self, key, value):
        converter = self._converters.get(key, self._default_export)
        return converter(value, self.encoding)


def sng2sng():
    """Console script to transform an .sng file through the SNG class."""
    import sys
    if len(sys.argv) != 3:
        print('Usage: {} <input-file> <output-file>'.format(sys.argv[0]))
        sys.exit(1)
    with _open(sys.argv[2], 'wb') as output:
        open(sys.argv[1]).export(output)
