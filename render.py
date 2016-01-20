from secretary import Renderer
engine = Renderer()

def bool_to_list(boolean):
    if boolean:
        return [{}]
    return []

def inv_bool_to_list(boolean):
    if not boolean:
        return [{}]
    return []

engine.environment.filters['bool_to_list'] = bool_to_list
engine.environment.filters['inv_bool_to_list'] = inv_bool_to_list

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


data = {

}
if __name__ == "__main__":
    result = render_odt('Land Transfer Tax Statement', data)
    with open('./.tmp/out.odt', 'wb') as f:
        f.write(result)
