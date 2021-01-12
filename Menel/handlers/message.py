import re

import discord
from cliffs import CommandDispatcher

from command_dispatcher.dispatch import dispatch
from objects.bot import Menel
from objects.cooldowns import cooldowns
from objects.message import Message


def setup(bot: Menel, cliffs: CommandDispatcher):
    @bot.event
    async def on_message(m: discord.Message):
        m = Message(m)

        print(f'{m.guild}\t{m.channel}\t{m.author}{(" -> " + m.clean_content) if m.content else ""}')

        if m.author.bot or not m.guild:
            return

        prefix = '.'

        if re.fullmatch(f'^<@!?{bot.user.id}>$', m.content, re.IGNORECASE):
            if not cooldowns.auto(m.author.id, '_mention', 3):
                await m.channel.send('Cześć')
            return

        if not m.content.lower().startswith(prefix):
            return

        await dispatch(cliffs, m, prefix)