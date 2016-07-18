import unittest
from render import render_odt
import json



class TestRender(unittest.TestCase):

    def test_0001_letter_template(self):
        data = {
            "company": {
                "companyName": "test",
                "companyNumber": "1"
            },
            "transaction": {
                "shareClass": "x",
                "amount": 100,
                "consideration": 1,
                "effectiveDateString": "16th March 2012"
            },
            "transferors": [{"name": "Guy", "address": "house"}],
            "transferorSignatories": [{"name": "Guy", "address": "house"}],
            "transferees": [{"name": "Mitch", "address": "house"}],
            "transfereeSignatories": [{"name": "Mitch", "address": "house"}],


        }
        render_odt('transfer', data, subdir='goodcompanies')



if __name__ == '__main__':
    unittest.main()
