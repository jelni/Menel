from os import getenv

import aiohttp

from functions.clean_content import clean_content


def setup(cliffs):
    @cliffs.command('pxseu <message...>', name='pxseu', cooldown=5)
    async def command(m, message):
        async with aiohttp.request(
                'POST', 'https://www.pxseu.com/api/v2/sendMessage',
                json={'message': message},
                headers={'Authorization': getenv('PXSEU_MESSAGE_TOKEN')},
                timeout=aiohttp.ClientTimeout(total=10)
        ) as r:
            if r.status == 200:
                await m.send('good')
            else:
                await m.send(clean_content((await r.json())['message']))