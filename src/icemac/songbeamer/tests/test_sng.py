# -*- coding: utf-8 -*-
# Copyright (c) 2012 Michael Howitz
# See also LICENSE.txt

from .. import ENCODING
import unittest

SIMPLE = """\
#Title=Mÿ nïcë=tïtlë
#Description=I wröte ä söng ...
---
Textüäl cöntents
inclüdig newlines
---
Möre text
""".encode(ENCODING)

CONVERTING_VALUES = """\
#Categories=füü bär, asdf
#Version=3
---
""".encode(ENCODING)


class SngParseTests(unittest.TestCase):
    """Testing ..sng.SNG.parse()."""

    def callFUT(self, stream):
        from io import BytesIO
        from ..sng import SNG
        return SNG.parse(BytesIO(stream)).data

    def test_parses_head_and_text_into_dict(self):
        self.assertEqual(
            {'Text': ['Textüäl cöntents',
                      'inclüdig newlines',
                      '---',
                      'Möre text'],
             'Title': 'Mÿ nïcë=tïtlë',
             'Description': 'I wröte ä söng ...'},
            self.callFUT(SIMPLE))

    def test_post_processes_some_keys(self):
        self.assertEqual(
            {'Text': [],
             'Categories': ['füü bär', 'asdf'],
             'Version': 3
                }, self.callFUT(CONVERTING_VALUES))


class SngPropertiesTests(unittest.TestCase):
    """Testing .sng.SNG's properties."""

    def callPUT(self, name, raw_value, conv_value):
        from ..sng import SNG
        sng = SNG()
        setattr(sng, name, raw_value)
        self.assertEqual(conv_value, sng.data[name])
        self.assertEqual(raw_value, getattr(sng, name))

    def test_Title(self):
        self.callPUT('Title', 'Tïtlë'.encode(ENCODING), 'Tïtlë')

    def test_Text(self):
        self.callPUT('Text', b'a\r\nb', ['a', 'b'])

    def test_Version(self):
        self.callPUT('Version', b'3', 3)

    def test_LangCount(self):
        self.callPUT('LangCount', b'1', 1)

    def test_Categories(self):
        self.callPUT('Categories',
                     'föö, bar baz'.encode(ENCODING),
                     ['föö', 'bar baz'])
        self.callPUT('Categories', b'qwe', ['qwe'])

    def test_Comments(self):
        self.callPUT('Comments', b'5HNkZg==', 'äsdf')

    def test_Chords(self):
        self.callPUT('Chords',
                     b'MTMsMCxEDTcsMTAsRQ0=',
                     [['13', '0', 'D'], ['7', '10', 'E']])
