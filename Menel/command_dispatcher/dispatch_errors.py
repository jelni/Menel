from math import ceil

from cliffs import MismatchedLiteralSuggestion, MismatchedParameterType

from functions.clean_content import clean_content
from functions.plural_time import plural_time


def cooldown(time: float) -> str:
    return f'Poczekaj jeszcze {plural_time(ceil(time))} przed ponownym użyciem komendy.'


def mismatched_parameter_type(e: MismatchedParameterType) -> str:
    return f'Wartość `{clean_content(e.actual.value)}` nie jest ' + {
        'int': 'liczbą całkowitą',
        'float': 'liczbą',
    }.get(e.expected.typename, f'typu `{e.expected.typename}`')


def mismatched_literal_suggestion(e: MismatchedLiteralSuggestion) -> str:
    return f'Masz na myśli `{clean_content(e.expected.value)}`?'