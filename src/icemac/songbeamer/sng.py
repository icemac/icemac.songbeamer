# Copyright (c) 2012 Michael Howitz
# See also LICENSE.txt
from . import ENCODING
from base64 import b64encode, b64decode
import inspect
import re


HEADLINE_RE = re.compile(b'^#(.*?)=(.*)$')


int_to_bytes = lambda x: bytes(str(x), ENCODING)


# Properties which convert the data on set and get, so the presented value
# is always the one from/for the .sng file, the converted is stored in
# SNG.data
CONVERTING_PROPERTIES = [
    # name, get converter, set converter
    ('Text', lambda x: ('\r\n'.join(x)).encode(ENCODING),
             lambda x: x.decode(ENCODING).splitlines()),
    ('Version', int_to_bytes, int),
    ('LangCount', int_to_bytes, int),
    ('Comments', lambda x: b64encode(x.encode(ENCODING)),
                 lambda x: b64decode(x).decode(ENCODING)),
    ('Categories', lambda x: b', '.join(y.encode(ENCODING) for y in x),
                   lambda x: [y.decode(ENCODING) for y in x.split(b', ')]),
    ('Chords', lambda x: b64encode(
        ('\r'.join(','.join(y) for y in x)).encode(ENCODING) + b'\r'),
               lambda x: [
                   y.split(',')
                   for y in b64decode(x).decode(ENCODING).splitlines()]),
    ]


def getter_factory(name, converter):
    """Creates a getter for the converting property, reading pythonic value
    from self.data and converting it to the value in .sng file"""
    def getter(self):
        return converter(self.data[name])
    return getter


def setter_factory(name, converter):
    """Creates a setter for the converting property, storing a pythonic value
    in self.data."""
    def setter(self, value):
        self.data[name] = converter(value)
    return setter


class SNGMeta(type):
    """Meta class defining converting properties for .sng files."""

    def __new__(mcs, name, bases, dict):
        for name, get_converter, set_converter in CONVERTING_PROPERTIES:
            dict[name] = property(fget=getter_factory(name, get_converter),
                                  fset=setter_factory(name, set_converter))
        return type.__new__(mcs, name, bases, dict)


class SNG(metaclass=SNGMeta):
    """Class describing a .sng file."""

    def __init__(self):
        self.__dict__['data'] = {}

    @classmethod
    def parse(cls, byte_stream):
        """Parse the contents of a .sng file to a dict."""
        data = byte_stream.read()
        head, text = data.split(b'---', 1)
        instance = cls()
        instance.Text = text.strip()
        instance._parse_head(head.splitlines())
        return instance

    def export(self, byte_stream):
        for key in self.data:
            if key == 'Text':
                # Text needs to be the last line
                continue
            byte_stream.write(
                b'#'+key.encode(ENCODING)+b'='+getattr(self, key)+b'\r\n')
        byte_stream.write(b'---\r\n')
        byte_stream.write(self.Text)

    def _parse_head(self, lines):
        for line in lines:
            key, value = HEADLINE_RE.search(line).groups()
            key = key.decode(ENCODING)
            setattr(self, key, value)

    def __setattr__(self, key, value):
        # Caution: This __setattr__ is called always even if there are
        # attributes or setter properties, so we have to handle the
        # properties in a special way:
        prop = inspect.getattr_static(self, key, None)
        if prop:
            # If there is a converting property, use it:
            prop.fset(self, value)
        else:
            # There is no property for key, so store it plain:
            self.data[key] = value.decode(ENCODING)

    def __getattr__(self, key):
        return self.data[key].encode(ENCODING)


def sng2sng():
    """Console script to transform an .sng file through the SNG class."""
    import sys
    if len(sys.argv) != 3:
        print('Usage: {} <input-file> <output-file>'.format(sys.argv[0]))
        sys.exit(1)
    with open(sys.argv[1], 'rb') as input:
        with open(sys.argv[2], 'wb') as output:
            SNG.parse(input).export(output)
