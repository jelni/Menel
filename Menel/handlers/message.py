import re

import discord
from cliffs import CommandDispatcher

import regexes
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

        if re.fullmatch(regexes.mention(bot.user.id), m.content):
            if not cooldowns.auto(m.author.id, '_mention', 3):
                await m.channel.send('Cześć')

        elif m.content.lower().startswith(prefix):
            await dispatch(cliffs, m, prefix)

        elif match := re.match(regexes.mention(bot.user.id), m.content):
            await dispatch(cliffs, m, match.group())