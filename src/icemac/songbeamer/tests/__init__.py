# Copyright (c) 2012 Michael Howitz
# See also LICENSE.txt


def additional_tests():
    # needed function to find doctests when runing `python setup.py test`
    from .test_doctests import test_suite
    return test_suite()
