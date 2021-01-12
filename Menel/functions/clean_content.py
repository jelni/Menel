from typing import Union

from discord.utils import escape_markdown, escape_mentions


def clean_content(content: Union[str, any], *, markdown: bool = True, mentions: bool = True) -> str:
    if not isinstance(content, str):
        content = str(content)

    if markdown:
        content = escape_markdown(content)
    if mentions:
        content = escape_mentions(content)

    return content