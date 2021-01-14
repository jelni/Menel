import discord

from objects.message import Message


def user_perms(m: Message) -> int:
    if m.author.id == m.bot.OWNER:
        return 5  # bot owner
    elif m.author == m.guild.owner:
        return 4  # guild owner
    elif m.channel.permissions_for(m.author).is_superset(discord.Permissions(8)):
        return 3  # admin
    elif m.channel.permissions_for(m.author).is_superset(discord.Permissions(32)):
        return 2  # manage server
    else:
        return 0  # normal user