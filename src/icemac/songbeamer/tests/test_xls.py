from .. import SNG
from .. xls import get_xlwt
from .. xls import main
from unittest import mock
import builtins
import pytest
import xlrd
import xlwt


def test_xls__get_xlwt__1():
    """It returns the `xlwt` module."""
    assert get_xlwt() == xlwt


def test_xls__get_xlwt__2(capfd):
    """It exits with an error message if xlwt cannot be imported."""
    with pytest.raises(SystemExit):
        with mock.patch.object(
                builtins, '__import__', side_effect=ImportError):
            get_xlwt()
    out, err = capfd.readouterr()
    assert out.startswith(
        'You have to install the `xls` extra for this feature.')


def test_xls__main__1(capfd):
    """It requires a source directory."""
    with pytest.raises(SystemExit) as err:
        main(['i-do-not-exist'])
    assert '2' == str(err.value)
    out, err = capfd.readouterr()
    assert err.strip().endswith("'i-do-not-exist' is not a valid path.")


def test_xls__main__2(tmpdir, capfd):
    """It requires a readable source directory."""
    dir = tmpdir.mkdir('not-readable')
    dir.chmod(0o000)
    with pytest.raises(SystemExit) as err:
        main([str(dir)])
    assert '2' == str(err.value)
    out, err = capfd.readouterr()
    assert err.strip().endswith("/not-readable' is not a readable dir.")


def test_xls__main__3(tmpdir, capfd):
    """It requires a target file."""
    with pytest.raises(SystemExit) as err:
        main([str(tmpdir)])
    assert '2' == str(err.value)
    out, err = capfd.readouterr()
    assert err.strip().endswith(
        "the following arguments are required: dest_file")


def test_xls__main__4(tmpdir, caplog):
    """It writes titles and numbers alphabetically sorted to an XLS file."""
    caplog.clear()
    base_dir = tmpdir.mkdir('sb-files')
    s1 = SNG()
    s1.update({
        'Title': 'Beta',
        'Songbook': 'SB 23',
        'ChurchSongID': 'CS 45',
        'Text': 'song text'
    })
    s1.export(base_dir.join('1.sng').open('wb'))

    s2 = SNG()
    s2.update({
        'Title': 'Alpha',
    })
    s2.export(base_dir.join('2.sng').open('wb'))

    s3 = SNG()
    s3.update({
        'ChurchSongID': 'CS 2411',
    })
    s3.export(base_dir.join('3.sng').open('wb'))

    base_dir.join('no.sng').write_binary('Nö sôñg!'.encode('latin-1'))
    dest_file = tmpdir.join('export.xls')

    main([str(base_dir), str(dest_file)])

    wb = xlrd.open_workbook(str(dest_file))
    assert [u'SongBeamer songs'] == wb.sheet_names()
    work_sheet_0 = wb.sheet_by_index(0)
    assert (3, 3) == (work_sheet_0.nrows, work_sheet_0.ncols)
    got = [work_sheet_0.row_values(rx)
           for rx in range(work_sheet_0.nrows)]
    assert [
        ['', 'CS 2411', ''],
        ['Alpha', '', ''],
        ['Beta', 'CS 45', 'SB 23'],
    ] == got
    assert "Missing Title in '3.sng'" in caplog.text
