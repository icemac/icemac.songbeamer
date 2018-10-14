# -*- coding: utf-8 -*-
from .. import ENCODING
from ..sng import SNG
from io import BytesIO
import difflib
import io
import os
import pkg_resources
import sys
import tempfile
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

SIMPLE_parsed = {'Text': ['Textüäl cöntents',
                          'inclüdig newlines',
                          '---',
                          'Möre text'],
                 'Title': 'Mÿ nïcë=tïtlë',
                 'Description': 'I wröte ä söng ...'}


class SngParseTests(unittest.TestCase):
    """Testing ..sng.SNG.parse()."""

    def callFUT(self, data):
        return SNG.parse(data).data

    def test_parses_head_and_text_into_dict_from_bytes(self):
        self.assertEqual(SIMPLE_parsed, self.callFUT(SIMPLE))

    def test_post_processes_some_keys(self):
        self.assertEqual({
            'Text': [],
            'Categories': ['füü bär', 'asdf'],
            'Version': 3
        }, self.callFUT(CONVERTING_VALUES))


def test_sng__SNG__parse__2():
    """It returns `None` if the file is not parsable."""
    assert SNG.parse('äöü'.encode(ENCODING)) is None


def test_sng__SNG__open__1(tmpdir):
    """It parses head and text into a dict from a file path."""
    tmpdir.join('simple.sng').write_binary(SIMPLE)
    assert SIMPLE_parsed == SNG.open(str(tmpdir.join('simple.sng'))).data


class SngPropertiesTests(unittest.TestCase):
    """Testing ..sng.SNG's properties."""

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


class SngExportTests(unittest.TestCase):
    """Testing ..sng.SNG.export()."""

    def test_export_converts_data_back_to_byte_stream(self):
        from .. import SNG

        sng = SNG()
        sng.data.update({
            'Version': 3,
            'Categories': ['foo bar', 'baz'],
            'Text': ['Textüäl cöntents',
                     'inclüdig newlines',
                     '---',
                     'Möre text'],
            'Title': 'Mÿ nïcë=tïtlë'})
        export_result = BytesIO()
        sng.export(export_result)
        self.assertEqual(
            '#Categories=foo bar, baz\r\n'
            '#Title=Mÿ nïcë=tïtlë\r\n'
            '#Version=3\r\n'
            '---\r\n'
            'Textüäl cöntents\r\n'
            'inclüdig newlines\r\n'
            '---\r\n'
            'Möre text'.encode(ENCODING), export_result.getvalue())


def test_sng__SNG__export__2():
    """It does not break if there is no `Text` in the song."""
    song = SNG()
    song.data['Title'] = 'my title'
    export_result = BytesIO()
    song.export(export_result)
    assert ('#Title=my title\r\n'
            '---\r\n'.encode(ENCODING) == export_result.getvalue())


class Sng2sngTests(unittest.TestCase):
    """Testing ..sng.sng2sng()."""

    def callFUT(self, *args):
        from ..sng import sng2sng
        orig_stdout = sys.stdout
        orig_argv = sys.argv[:]
        stdout = io.StringIO()
        argv = ['sng2sng']
        argv.extend(args)
        try:
            sys.stdout = stdout
            sys.argv[:] = argv
            try:
                sng2sng()
            except SystemExit as e:
                raise SystemExit(str(e), stdout.getvalue())
        finally:
            sys.stdout = orig_stdout
            sys.argv[:] = orig_argv

    def test_wrong_number_of_args_leads_to_error_message(self):
        with self.assertRaises(SystemExit) as err:
            self.callFUT('input.sng')
        self.assertEqual(('1', 'Usage: sng2sng <input-file> <output-file>\n'),
                         err.exception.args)

    def test_output_is_equal_input_after_conversion(self):
        # Caution: keys in `in_filename` are sorted, because export sorts
        # keys alphabetically to be compatible across python versions!
        in_filename = pkg_resources.resource_filename(
            'icemac.songbeamer.tests', 'example.sng')
        try:
            out_fd, out_filename = tempfile.mkstemp()
            os.close(out_fd)
            self.callFUT(in_filename, out_filename)
            with open(in_filename, 'r') as in_file:
                in_file_cont = in_file.readlines()
            with open(out_filename, 'r') as out_file:
                out_file_cont = out_file.readlines()
            # There are no differences between input and output:
            self.assertEqual(
                [], list(difflib.context_diff(in_file_cont, out_file_cont)))
        finally:
            os.unlink(out_filename)
