"""
Cuba B
Nov 7, 2021
tests.py
"""

import unittest
from twitter_data import UrlMaker


class TestAuth(unittest.TestCase):
    """
    Test cases for Auth class
    """
    def test_urlMarker(self):
        ids = [234, 5456, 78908]
        arr_obj = UrlMaker(ids).create()
        print(arr_obj)


if __name__ == '__main__':
    unittest.main()


