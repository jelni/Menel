import itertools
from typing import Mapping, Optional

import discord
from discord.ext import commands as dc_commands

from ..objects.context import Context
from ..utils.formatting import code, codeblock
from ..utils.text_tools import user_input


def command_category(command: dc_commands.Command) -> str:
    cog = command.cog
    return cog.qualified_name if cog is not None else 'Bot'


def command_category_and_name(command: dc_commands.Command) -> tuple[str, str]:
    return command_category(command), command.qualified_name


def sort_and_filter_commands(commands: set[dc_commands.Command]) -> list[dc_commands.Command]:
    return sorted(filter(lambda c: not c.hidden, commands), key=command_category_and_name)


def group_categories(commands: list[dc_commands.Command]) -> itertools.groupby:
    return itertools.groupby(commands, key=command_category)


class HelpCommand(dc_commands.HelpCommand):
    context: Context
    remove_mentions = staticmethod(user_input)

    def __init__(self):
        super().__init__(
            command_attrs={
                'description': 'Wyświetla pomoc',
                'help': 'command - komenda której pomoc chcesz uzyskać'
            }
        )

    async def send_bot_help(self, mapping: Mapping[Optional[dc_commands.Cog], list[dc_commands.Command]]) -> None:
        ctx = self.context

        embed = discord.Embed(
            title='Lista komend',
            description=f'Użyj `{ctx.clean_prefix}help [command]`, '
                        f'aby otrzymać więcej informacji o komendzie lub kategorii\n'
                        f'Ustawione prefixy: {await ctx.get_prefixes_str()}',
            colour=discord.Colour.green()
        )
        embed.set_thumbnail(url=ctx.bot.user.avatar.replace(4096))

        for category, commands in group_categories(sort_and_filter_commands(ctx.bot.commands)):
            embed.add_field(name=category, value=' '.join(code(c.name) for c in commands), inline=False)

        await ctx.send(embed=embed)

    async def send_cog_help(self, cog: dc_commands.Cog) -> None:
        ctx = self.context

        commands = sort_and_filter_commands(cog.get_commands())
        if not commands:
            await ctx.error(self.category_has_no_commands())
            return

        commands_text = []
        for command in commands:
            commands_text.append(f'`{command.qualified_name}` \N{EM DASH} {command.description}')

        await ctx.send(
            embed=discord.Embed(
                title=cog.qualified_name,
                description=f'{cog.description}\n\n' + '\n'.join(commands_text),
                colour=discord.Colour.green()
            )
        )

    async def send_group_help(self, group: dc_commands.Group) -> None:
        ctx = self.context

        commands = sort_and_filter_commands(group.commands)

        commands_text = []
        for command in commands:
            commands_text.append(f'`{command.name}` \N{EM DASH} {command.description}')

        await ctx.send(
            embed=discord.Embed(
                title=group.qualified_name,
                description=f'{group.description}\n\n' + '\n'.join(commands_text),
                colour=discord.Colour.green()
            )
        )

    async def send_command_help(self, command: dc_commands.Command) -> None:
        ctx = self.context

        text = [command.description, codeblock(f'{ctx.clean_prefix}{command.qualified_name} {command.signature}')]
        if command.help:
            text.append(command.help)

        embed = discord.Embed(
            title=command.qualified_name,
            description='\n'.join(text),
            colour=discord.Colour.green()
        )
        if command.aliases:
            embed.add_field(name='Aliasy', value=' '.join(map(code, command.aliases)))
        try:
            can_run = await command.can_run(ctx)
        except dc_commands.CommandError:
            can_run = False
        embed.add_field(name='Masz wystarczające uprawnienia', value='Tak' if can_run else 'Nie')
        await ctx.send(embed=embed)

    async def send_error_message(self, error: str) -> None:
        await self.context.error(error)

    def command_not_found(self, name: str) -> str:
        return f'Nie znaleziono komendy {name}'

    def subcommand_not_found(self, command: dc_commands.Command, name: str) -> str:
        if isinstance(command, dc_commands.Group):
            return f'Komenda **{command.qualified_name}** nie ma subkomendy o nazwie {name}'
        return f'Komenda **{command.qualified_name}** nie ma subkomend'

    @staticmethod
    def category_has_no_commands() -> str:
        return 'Ta kategoria nie ma żadnych komend'