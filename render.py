from secretary import Renderer
engine = Renderer()


def join_and(items=[], attribute=None):
    if attribute:
        items = map(lambda x: x.get(attribute), items)
    if not len(items):
        return 'UNKNOWN'
    elif len(items) == 1:
        return items[0] or 'UNKNOWN'
    return '%s and %s' % (', '.join(items[:len(items)-1]), items[-1])


engine.environment.filters['join_and'] = join_and


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
