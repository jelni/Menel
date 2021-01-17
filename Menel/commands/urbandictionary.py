import re
from urllib import parse

import aiohttp
import discord

from ..functions.clean_content import clean_content
from ..functions.cut_long_text import cut_long_text
from ..objects.message import Message


def setup(cliffs):
    @cliffs.command('(urbandictionary|urban|ud) <query...>', name='urbandictionary', cooldown=5)
    async def command(m: Message, query):
        async with m.channel.typing():
            async with aiohttp.request(
                    'HEAD', f'https://www.urbandictionary.com/define.php?term={parse.quote(query)}',
                    allow_redirects=False,
                    timeout=aiohttp.ClientTimeout(total=10)
            ) as r:
                if r.status == 200:
                    query = parse.quote(query)
                elif r.status == 302:
                    query = r.headers['Location'].split('?term=', 1)[1]
                else:
                    await m.error('Nie znalazłem tej frazy w Urban Dictionary.')
                    return

            async with aiohttp.request(
                    'GET', f'https://api.urbandictionary.com/v0/define?term={query}',
                    timeout=aiohttp.ClientTimeout(total=10)
            ) as r:
                json = await r.json()

            json = json['list'][0]


            def remove_brackets(text: str) -> str:
                return re.sub(r'\[(?P<link>.*?)]', r'\g<link>', text)


            embed = discord.Embed(
                title=cut_long_text(json['word'], 256),
                url=json['permalink'],
                description=cut_long_text(clean_content(remove_brackets(json['definition'])), 1024)
            )

            embed.add_field(
                name='Example',
                value=cut_long_text(clean_content(remove_brackets(json['example'])), 1024),
                inline=False
            )

            embed.set_footer(text=f'Author: {clean_content(json["author"])}\n'
                                  f'👍 {json["thumbs_up"]} 👎 {json["thumbs_down"]}')

            await m.send(embed=embed)