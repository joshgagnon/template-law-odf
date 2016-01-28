import unittest
from render import render_odt
from collections import defaultdict

d = defaultdict(dict)

default_data = {
    "contactMethod": {
        "email": "as",
        "method": "email"
    },
    "dateString": "08 January 2016",
    "documents": [
        "asdfdasf",
        "sdfsadf"
    ],
    "fee": {
        "feeType": "none"
    },
    "fileType": "odt",
    "mappings": {
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
    },
    "matter": {
        "description": "s",
        "matterId": "as",
        "name": "asdf",
        "matterType": "taco"
    },
    "recipient": {
        "individuals": [
            {
                "firstName": "sadf",
                "lastName": "df"
            }
        ],
        "recipientType": "individuals"
    },
    "sender": "Thomas Bloy",
    "subject": "asdf",
    "valediction": "sincerely"
}


class TestRender(unittest.TestCase):

    def test_0001_letter_template(self):
        render_odt('G01: Letter', default_data)

    def test_0002_letter_of_engagement(self):
        render_odt('G02: Letter of Engagement', default_data)

    def test_0003_file_closing_letter(self):
        render_odt('G03: File Closing Letter', default_data)

    def test_0004_letter_of_engagment_conveyancing(self):
        render_odt('CV01: Letter of Engagement - Conveyancing', default_data)

    def test_0005_settlment_undertakings_letter(self):
        render_odt('CV03: Settlement Undertakings Letter - Acting for Purchaser', default_data)



if __name__ == '__main__':
    unittest.main()