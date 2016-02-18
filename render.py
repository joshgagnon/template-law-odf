from secretary import Renderer
import datetime
import inflect

inflect_engine = inflect.engine()

engine = Renderer()


def join_and(items=[], *attributes):
    print items, attributes
    if attributes:
        items = [' '.join(filter(lambda x: x, map(lambda attr: i.get(attr, ''), attributes))) for i in items]
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


def sum_debits_credits(args, debits=True, credits=True):
    total = 0
    for arg in args:
        if debits and arg and arg.get('debit'):
            total -= arg.get('debit', 0)
        if credits and arg and arg.get('credit'):
            total += arg.get('credit', 0)
    return total if debits and credits else abs(total)


def format_number(number):
    return '{:,.2f}'.format(number or 0)


def currency(string):
    if string and string[0] == '$':
        return string
    return '$%s' % string


def percentage(string):
    if string and string[-1] == '%':
        return string
    return '%s%%' % string


def number_to_words(num):
    return inflect_engine.number_to_words(num or 0)

engine.environment.filters['join_and'] = join_and
engine.environment.filters['week_day'] = week_day
engine.environment.filters['sum_debits_credits'] = sum_debits_credits
engine.environment.filters['format_number'] = format_number
engine.environment.filters['currency'] = currency
engine.environment.filters['percentage'] = percentage
engine.environment.filters['number_to_words'] = number_to_words


def render_odt(form_name, values):
    with open('templates/' + form_name + '.odt') as template:
        result = engine.render(template, **values)
    return result
