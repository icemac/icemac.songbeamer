# Copyright (c) 2012 Michael Howitz
# See also LICENSE.txt
import doctest
import os
import os.path


def setUp(test):
    test._old_cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))


def tearDown(test):
    os.chdir(test._old_cwd)


optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.REPORT_NDIFF |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    return doctest.DocFileSuite(
        'USAGE.txt',
        package="icemac.songbeamer",
        setUp=setUp,
        tearDown=tearDown,
        optionflags=optionflags)
