from ..objects.bot import Menel


def setup(bot: Menel):
    @bot.event
    async def on_shard_connect(shard_id):
        print(f'Connected on shard {shard_id}')