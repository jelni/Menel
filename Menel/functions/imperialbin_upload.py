from os import getenv

import aiohttp


async def imperialbin_upload(
        text: str, *, longer_urls: bool, instant_delete: bool, image_embed: bool, expiration: int
) -> dict:
    async with aiohttp.request(
            'POST', 'https://imperialb.in/api/postCode/',
            json={
                'code': text,
                'apiToken': getenv('IMPERIALBIN_TOKEN'),
                'longerUrls': longer_urls,
                'instantDelete': instant_delete,
                'imageEmbed': image_embed,
                'expiration': expiration
            },
            headers={'User-Agent': 'Menel Discord Bot; (https://github.com/JelNiSlaw/Menel)'},
            timeout=aiohttp.ClientTimeout(total=20)
    ) as r:
        return await r.json()