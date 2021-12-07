"""
Cuba B
Nov 7, 2021
test_locNum.py
"""

import unittest
from twitter_data import LocationNumber


class TestAuth(unittest.TestCase):
    """
    Test cases for Auth class
    """
    def test_locNum(self):
        ids = ['Boston', 'Manchester', 'Dallas']
        arr_obj = LocationNumber(ids).get_location()
        print(arr_obj)


if __name__ == '__main__':
    unittest.main()
