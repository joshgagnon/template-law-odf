from secretary import Renderer
import logging
logging.basicConfig()

data =  { "dateString": "14 January 2016",

    "recipient": {
        "individuals": [
            {
                "firstName": "Mike",
                "lastName": "Jones"
            },
            {
                "firstName": "Denny",
                "lastName": "Dennysingers"
            }
        ],
        "recipientType": "individuals",
        "email": "kapow@pewpew.com",
        "address": {
            "street": "90 Power Ave",
            "suburb": "Kingbo",
            "postcode": "9666",
            "city": "Sincity",
            "country": "Atroika"
        },
    },
    "matter": {
        "matterType": "purchase",
        "assets": [
            {
                "address": "60 Binge St"
            },
            {
                "address": "66 Catwalk Blv"
            }]
    },
    "sender": "Thomas Bloy",
        "mappings": {
        "price": {
            "purchase": "$880",
            "sale": "$780",
            "refinance": "$680"
        },
        "sender": {
            "Thomas Bloy": {
                "phone": "+64 274 538 552",
                "title": "Director",
                "email": "thomas@evolutionlawyers.nz"
            },
            "Tamina Cunningham-Adams": {
                "phone": "+64 021 1515 137",
                "title": "Director",
                "email": "tamina@evolutionlawyers.nz"
            }
        }
    }
}



engine = Renderer()


with open('templates/Letter of Engagement.odt') as template, open('out.odt', 'wb') as out:
    result = engine.render(template, **data)
    out.write(result)