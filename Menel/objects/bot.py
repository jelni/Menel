import discord
from discord import AutoShardedClient


class Menel(AutoShardedClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ready = False

        self.config = dict()
        self.db = None
        self.word_lists = None

        self.cooldowns = {}


bot = Menel(
    max_messages=10000,
    intents=discord.Intents(
        guilds=True,
        members=True,
        bans=False,
        emojis=False,
        integrations=False,
        webhooks=False,
        invites=False,
        voice_states=False,
        presences=False,
        messages=True,
        reactions=False,
        typing=False
    ),
    member_cache_flags=discord.MemberCacheFlags(online=False, voice=False, joined=True),
    chunk_guilds_at_startup=True,
    status=discord.Status.online,
    activity=discord.Activity(name='scam', type=discord.ActivityType.watching),
    allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True),
    heartbeat_timeout=10,
    guild_ready_timeout=5,
    guild_subscriptions=True
)