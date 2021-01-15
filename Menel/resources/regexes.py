import re


DISCORD_BOT_TOKEN = re.compile(r'(?:[\w\-=]+)\.(?:[\w\-=]+)\.(?:[\w\-=]+)', re.ASCII)


def mention(user_id: int) -> re.Pattern:
    return re.compile(rf'<@!?{user_id}>', re.IGNORECASE | re.ASCII)