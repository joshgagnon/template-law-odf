from secretary import Renderer
import datetime

engine = Renderer()


def join_and(items=[], attribute=None):
    if attribute:
        items = map(lambda x: x.get(attribute), items)
    if not len(items):
        return 'UNKNOWN'
    elif len(items) == 1:
        return items[0] or 'UNKNOWN'
    return '%s and %s' % (', '.join(items[:len(items) - 1]), items[-1])


def week_day(date_string):
    try:
        return datetime.datetime.strptime(date_string, '%d %B %Y').strftime('%A')
    except ValueError:
        return 'UNKNOWN'


engine.environment.filters['join_and'] = join_and
engine.environment.filters['week_day'] = week_day


def render_odt(form_name, values):
    with open('templates/' + form_name + '.odt') as template:
        result = engine.render(template, **values)
    return result
