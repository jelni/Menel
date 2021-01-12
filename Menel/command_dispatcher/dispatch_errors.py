from cliffs import MismatchedLiteralSuggestion, MismatchedParameterType
from discord import Colour, Embed

from functions.clean_content import clean_content


def mismatched_parameter_type(e: MismatchedParameterType) -> Embed:
    return Embed(
        description=f'Wartość `{clean_content(e.actual.value)}` nie jest ' +
                    {
                        'int': 'liczbą całkowitą',
                        'float': 'liczbą',
                    }.get(e.expected.typename, f'typu `{e.expected.typename}`'),
        colour=Colour.red()
    )


def mismatched_literal_suggestion(e: MismatchedLiteralSuggestion) -> Embed:
    return Embed(description=f'Masz na myśli `{clean_content(e.expected.value)}`?')