import unittest
from render import render_odt
from collections import defaultdict
import json


mappings = {
    "sender": {
        "Tamina Cunningham-Adams": {
            "email": "tamina@evolutionlawyers.nz",
            "phone": "+64 021 1515 137",
            "title": "Director"
        },
        "Thomas Bloy": {
            "email": "thomas@evolutionlawyers.nz",
            "phone": "+64 274 538 552",
            "title": "Director"
        }
    },
    "price": {}
}


class TestRender(unittest.TestCase):

    def test_0001_letter_template(self):
        with open('fixtures/G01.json') as data:
            render_odt('G01: Letter', dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0002_letter_of_engagement(self):
        with open('fixtures/G02.json') as data:
            render_odt('G02: Letter of Engagement', dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0003_file_closing_letter(self):
        with open('fixtures/G03.json') as data:
            render_odt('G03: File Closing Letter', dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0004_letter_of_engagment_conveyancing(self):
        with open('fixtures/CV01.json') as data:
            render_odt('CV01: Letter of Engagement - Conveyancing', dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0005_settlment_undertakings_letter(self):
        with open('fixtures/CV03.json') as data:
            render_odt('CV03: Settlement Undertakings Letter - Acting for Purchaser', dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0006_settlment_undertakings_letter_vendor(self):
        with open('fixtures/CV04.json') as data:
            render_odt('CV04: Settlement Undertakings Letter - Acting for Vendor', dict(json.loads(data.read()).items() + [("mappings", mappings)]))


if __name__ == '__main__':
    unittest.main()