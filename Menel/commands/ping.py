import discord


def setup(cliffs):
    @cliffs.command('ping', name='ping')
    async def command(m):
        message = await m.send('Pong!')

        delay = round((message.created_at.timestamp() - m.created_at.timestamp()) * 1000)

        try:
            await message.edit(content=f'Ping: {delay}ms')
        except discord.HTTPException:
            pass