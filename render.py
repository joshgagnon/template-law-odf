from secretary import Renderer
engine = Renderer()


def render_odt(form_name, values):
    with open('templates/' + form_name + '.odt') as template:
        result = engine.render(template, **values)
    return result


data = {

    'linzDealingNumber': '893245978',
    #'actionstepId': 'asdfa'
    'recipient': {
        'recipientType': 'individual',
        'individuals': [{
            'firstName': 'Mike',
            'lastName': 'Paton'
                }, {
            'firstName': 'Jimmy',
            'lastName': 'Burns'
        }
        ],
        'corporateClient': True

    }
}

if __name__ == "__main__":
    result = render_odt('Authority & Instruction Form - Conveyancing', data)
    with open('./.tmp/out.odt', 'wb') as f:
        f.write(result)
