import discord
from discord.utils import escape_markdown, escape_mentions


def cut_long_text(text: str, max_length: int = 2000):
    if len(text) > max_length:
        return f'{text[:max_length - 1].rstrip()}…'
    else:
        return text


def constant_length_text(text: str, length: int):
    if len(text) > length:
        return text[:length - 1] + '…'
    else:
        return text.ljust(length, ' ')


def clean_content(content: any, *, markdown: bool = True, mentions: bool = True) -> str:
    if not isinstance(content, str):
        content = str(content)

    if markdown:
        content = escape_markdown(content)
    if mentions:
        content = escape_mentions(content)

    return content


def plural_word(count: int, one: str, few: str, many: str) -> str:
    if count == 1:
        word = one
    elif 10 <= count < 20:
        word = many
    else:
        last = count % 10

        if 1 < last < 5:
            word = few
        else:
            word = many

    return f'{count} {word}'


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


def stringify_permissions(permissions: discord.Permissions) -> str:
    return ', '.join(f'`{perm.replace("_", " ")}`' for perm, value in iter(permissions) if value)