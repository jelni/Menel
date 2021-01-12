import discord


class Message(discord.Message):
    def __init__(self, message: discord.Message):
        self.message = message


    def __getattr__(self, item):
        return self.message.__getattribute__(item)


    async def send(self, *args, **kwargs) -> discord.Message:
        try:
            return await self.channel.send(*args, **kwargs)
        except discord.Forbidden:
            pass
        except discord.HTTPException as e:
            return await self.channel.send(str(e))