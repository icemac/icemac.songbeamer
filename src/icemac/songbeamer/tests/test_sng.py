# -*- coding: utf-8 -*-
from .. import ENCODING
from .. import sng
from io import BytesIO
import difflib
import io
import os
import pkg_resources
import pytest
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
    """Testing ..sng.parse()."""

    def callFUT(self, data):
        return sng.parse(data)

    def test_parses_head_and_text_into_dict_from_bytes(self):
        self.assertEqual(SIMPLE_parsed, self.callFUT(SIMPLE))

    def test_post_processes_some_keys(self):
        self.assertEqual({
            'Text': [],
            'Categories': ['füü bär', 'asdf'],
            'Version': 3
        }, self.callFUT(CONVERTING_VALUES))


def test_sng__parse__2(caplog):
    """It returns `None` if the file is no SongBeamer file.

    It is logging the name of the file.
    """
    assert sng.parse('äöü'.encode(ENCODING), 'my-song.sng') is None
    assert ("'my-song.sng' cannot be parsed: it does not contain `---`."
            in caplog.text)


def test_sng__parse__3(caplog):
    """It returns `None` if the file contains invalid data structures.

    It is logging the name of the file.
    """
    assert sng.parse('a---b'.encode(ENCODING), 'my-song.sng') is None
    assert ("'my-song.sng' cannot be parsed: Invalid data structure in line 1:"
            " b'a'\n" in caplog.text)


def test_sng__parse__4():
    """It is able to parse files starting with a UTF-8 BOM."""
    song = sng.parse(b'\xef\xbb\xbf#Title=B\xc3\xa4r---Tek\xc3\x9ft')
    assert song is not None
    assert {'Title': 'Bär',
            'Text': ['Tekßt']} == song


def test_sng__open__1(tmpdir):
    """It parses head and text into a dict from a file path."""
    tmpdir.join('simple.sng').write_binary(SIMPLE)
    song = sng.open(str(tmpdir.join('simple.sng')))
    assert SIMPLE_parsed == song
    assert 'simple.sng' == song.filename


conversion_table = (
    ('Title', 'Tïtlë'.encode(ENCODING), 'Tïtlë'),
    ('Text', b'a\r\nb', ['a', 'b']),
    ('Version', b'3', 3),
    ('LangCount', b'1', 1),
    ('Categories', 'föö, bar baz'.encode(ENCODING), ['föö', 'bar baz']),
    ('Categories', b'qwe', ['qwe']),
    ('Comments', b'5HNkZg==', 'äsdf'),
    ('Chords', b'MTMsMCxEDTcsMTAsRQ0=', [['13', '0', 'D'], ['7', '10', 'E']]),
)


@pytest.mark.parametrize('key,input,output', conversion_table)
def test_sng___Importer__import__1(key, input, output):
    """It converts encoded values to text."""
    importer = sng._Importer(ENCODING)
    assert importer._import(key, input) == output


@pytest.mark.parametrize('key,output,input', conversion_table)
def test_sng___Exporter__export__1(key, output, input):
    """It converts text to encoded values."""
    importer = sng._Exporter(ENCODING, None, None)
    assert importer._export(key, input) == output


class SngExportTests(unittest.TestCase):
    """Testing ..sng.SNG.export()."""

    def test_export_converts_data_back_to_byte_stream(self):
        from .. import SNG

        sng = SNG()
        sng.update({
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
    song = sng.SNG()
    song['Title'] = 'my title'
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
