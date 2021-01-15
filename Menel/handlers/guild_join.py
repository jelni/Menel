from ..objects.bot import Menel


def setup(bot: Menel):
    @bot.event
    async def on_guild_join(guild):
        print(f'Joined server {guild}')