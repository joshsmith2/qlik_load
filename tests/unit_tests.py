__author__ = 'josh'

import unittest
import load_from_script
import os

class UnitTest(unittest.TestCase):

    def setUp(self):
        self.in_csv = "files/clutha_sample.csv"
        self.header_file = "../standard_contents/header.txt"
        self.out_file = "out.txt"
        self.conversion_file = "../standard_contents/conversion_table.csv"

        # Remove output
        if os.path.exists(self.out_file):
            os.remove(self.out_file)

    def tearDown(self):
        pass

    def test_headers(self):
        headers = load_from_script.get_headers(self.in_csv)
        self.assertTrue(len(headers) == 93)
        self.assertIn("twitter.tweet/truncated", headers)

    def test_ls_header(self):
        load_from_script.print_header(self.header_file, self.out_file)
        self.assertTrue(os.path.exists(self.out_file))
        with open(self.header_file, 'r') as hf:
            expected = hf.readlines()
        with open(self.out_file, 'r') as of:
            observed = of.readlines()
        self.assertEqual(expected, observed)

    def test_table_statement(self):
        headers = load_from_script.get_headers(self.in_csv)
        conversions = load_from_script.load_conversion_table(self.conversion_file)
        load_from_script.print_table_writer(self.out_file,
                                            headers,
                                            conversions,
                                            self.in_csv)
        self.assertTrue(os.path.exists(self.out_file))

    def test_loading_conversion(self):
        conv = load_from_script.load_conversion_table(self.conversion_file)
        expected_keys = {'field_from_csv', 'modifier', 'conversion'}
        found_keys = set(conv[0].keys())
        self.assertEqual(found_keys, expected_keys)
        self.assertEqual(len(conv), 92)