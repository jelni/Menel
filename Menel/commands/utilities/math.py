import aiohttp
import discord

from ...functions import clean_content, cut_long_text, embed_with_author
from ...objects import Category, Command, Message


COMMAND = Command(
    'math',
    syntax=None,
    description='Oblicza działanie matematyczne.',
    aliases=('m', 'calculate', 'calculator', 'calc'),
    category=Category.UTILS,
    cooldown=2
)


def setup(cliffs):
    @cliffs.command('(math|m|calculate|calculator|calc) <expression...>', command=COMMAND)
    async def command(m: Message, expression):
        async with m.channel.typing():
            async with aiohttp.request(
                    'POST', 'https://api.mathjs.org/v4/',
                    json={'expr': expression},
                    timeout=aiohttp.ClientTimeout(total=10)
            ) as r:
                json = await r.json()

            embed = embed_with_author(
                m.author,
                discord.Embed(description=clean_content(cut_long_text(json['error'] or json['result'])))
            )
            embed.colour = discord.Color.red() if json['error'] else discord.Color.green()
            embed.set_footer(text='Kalkulator Marcin Grobelkiewicz\nmath.js API actually')

            await m.send(embed=embed)