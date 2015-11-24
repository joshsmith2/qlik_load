__author__ = 'josh'

import unittest
import load_from_script

class UnitTest(unittest.TestCase):

    def setUp(self):
        self.in_csv = "files/clutha_sample.csv"

    def test_headers(self):
        headers = load_from_script.get_headers(self.in_csv)
        self.assertTrue(len(headers) == 93)
        self.assertIn("twitter.tweet/truncated", headers)