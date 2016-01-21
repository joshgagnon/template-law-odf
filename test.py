import unittest
from render import render_odt
from collections import defaultdict

d = defaultdict(dict)

default_data = {
    'recipient': d,
    'matter': d,
    'mappings': d
}

class TestRender(unittest.TestCase):

    def test_0001_letter_template(self):
        render_odt('Letter Template', default_data)

    def test_0002_letter_of_engagement(self):
        render_odt('Letter of Engagement', default_data)

    def test_0003_land_transfer_tax_statement(self):
        render_odt('Land Transfer Tax Statement', default_data)

if __name__ == '__main__':
    unittest.main()
