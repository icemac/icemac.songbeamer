import doctest


optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.REPORT_NDIFF |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    return doctest.DocFileSuite(
        'USAGE.rst',
        package="icemac.songbeamer",
        optionflags=optionflags)
