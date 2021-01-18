import imghdr
from io import BytesIO
from os import getenv

import aiohttp
import discord

from ..objects.message import Message


def setup(cliffs):
    @cliffs.command('jezus', name='jezus', cooldown=3)
    async def command(m: Message):
        async with aiohttp.request(
                'GET', 'https://api.badosz.com/jesus',
                headers={'Authorization': getenv('BADOSZ_TOKEN')},
                timeout=aiohttp.ClientTimeout(total=10)
        ) as r:
            if r.status == 200:
                file = BytesIO(await r.read())
                await m.send(file=discord.File(file, filename=f'jezus.{imghdr.what(file)}'))
            else:
                await m.error('Nie wiem, nie działa.')