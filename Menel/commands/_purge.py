from typing import Callable, Optional

import discord

from objects.message import Message


def setup(cliffs):
    @cliffs.command(
        '(purge|clear|prune) '
        '([all] <count: int>'
        '|user <text> <count: int>'
        '|bots <count: int>'
        '|humans <count: int>'
        '|files <count: int>'
        '|images <count: int>'
        '|embeds <count: int>'
        '|match <text> <count: int>'
        '|links <count: int>'
        '|mentions [<text>] <count: int>'
        '|startswith <text> <count: int>'
        '|endswith <text> <count: int>'
        '|invites <count: int>'
        '):mode',
        name='purge', cooldown=3
    )
    async def command(m: Message, mode: int, text: str = None, count: int = None):
        async def purge(limit: int, *, check: Optional[Callable] = None, after: discord.Message = None):
            await m.channel.purge(limit=limit, check=check, after=after)


        if mode == 0:
            await purge(count)