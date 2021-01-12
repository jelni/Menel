from objects.bot import Menel


def setup(bot: Menel):
    @bot.event
    async def on_guild_remove(guild):
        print(f'Left server {guild}')