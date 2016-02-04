import unittest
from render import render_odt
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
            render_odt('G01: Letter',
                       dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0002_letter_of_engagement(self):
        with open('fixtures/G02.json') as data:
            render_odt('G02: Letter of Engagement',
                       dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0003_file_closing_letter(self):
        with open('fixtures/G03.json') as data:
            render_odt('G03: File Closing Letter',
                       dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0004_letter_of_engagment_conveyancing(self):
        with open('fixtures/CV01.json') as data:
            render_odt('CV01: Letter of Engagement - Conveyancing',
                       dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0005_settlment_undertakings_letter(self):
        with open('fixtures/CV03.json') as data:
            render_odt('CV03: Settlement Undertakings Letter - Acting for Purchaser',
                       dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0006_settlment_undertakings_letter_vendor(self):
        with open('fixtures/CV04.json') as data:
            render_odt('CV04: Settlement Undertakings Letter - Acting for Vendor',
                       dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0007_mortgage(self):
        with open('fixtures/CV05.json') as data:
            render_odt('CV05: Mortgage Discharge Request',
                       dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0008_settlement(self):
        with open('fixtures/CV06.json') as data:
            render_odt('CV06: Vendors Settlement Letter',
                       dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0009_settlement(self):
        with open('fixtures/CV07.json') as data:
            render_odt('CV07: Letter to Financier Enclosing Originals',
                       dict(json.loads(data.read()).items() + [("mappings", mappings)]))

    def test_0010_trust_balance(self):
        for d in xrange(1, 3):
            with open('fixtures/CV10.%d.json' % d) as data:
                render_odt('CV10: Trust Account Statement',
                           dict(json.loads(data.read()).items() + [("mappings", mappings)]))

if __name__ == '__main__':
    unittest.main()
