"""
Zach, Evan, Cuba
test_urlmaker.py
December 7 2021
"""
import unittest
from class_container import LocationNumber
from class_container import UrlMaker


class Test1(unittest.TestCase):
    """
    Testcases
    """

    def test_case_1(self):
        """
        Test case for UrlMaker create
        """
        ids = (12783635, 68462931, 73946251)
        url_list = UrlMaker(ids).create()
        print(url_list)
        actual_result = url_list
        expected_result = [
            "https://twitter.com/twitter/statuses/12783635",
            "https://twitter.com/twitter/statuses/68462931",
            "https://twitter.com/twitter/statuses/73946251",
        ]
        self.assertEqual(actual_result, expected_result)

    def test_case_2(self):
        """
        Test case for UrlMaker shorten
        """
        ids = (67234908, 10937563, 79326074)
        url_list = UrlMaker(ids).create()
        short_links_list = UrlMaker(url_list).shorten()
        print(short_links_list)
        actual_result = short_links_list
        expected_result = [
            "https://tinyurl.com/y6ynona3",
            "https://tinyurl.com/y3jmvu2f",
            "https://tinyurl.com/yyh3eqxt",
        ]
        self.assertEqual(actual_result, expected_result)


if __name__ == "__main__":
    unittest.main()
