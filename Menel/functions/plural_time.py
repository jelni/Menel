from ..functions.plural_word import plural_word


def plural_time(number: int) -> str:
    if number >= 3600:
        number //= 3600
        unit = 'godzin'
    elif number >= 60:
        number //= 60
        unit = 'minut'
    else:
        unit = 'sekund'

    return plural_word(number, one=unit + 'ę', few=unit + 'y', many=unit)