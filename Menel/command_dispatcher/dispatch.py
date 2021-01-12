from cliffs import (
    CallMatchFail,
    CommandDispatcher,
    MismatchedLiteralSuggestion,
    MismatchedParameterType,
    UnknownCommandError
)

from command_dispatcher import dispatch_errors
from objects.cooldowns import cooldowns
from objects.message import Message


async def dispatch(cliffs: CommandDispatcher, m: Message, prefix: str):
    try:
        result, command = cliffs.dispatch(m.content[len(prefix):], m=m, prefix=prefix)
    except MismatchedLiteralSuggestion as e:
        await m.send(embed=dispatch_errors.mismatched_literal_suggestion(e))

    except MismatchedParameterType as e:
        await m.send(embed=dispatch_errors.mismatched_parameter_type(e))

    except CallMatchFail as fail:
        ...
        # if 'name' in fail.command.kwargs:
        #     await send(m.channel, commands.other.help.get_help(fail.command.kwargs['name'], prefix))

    except UnknownCommandError:
        pass
    else:
        if not result:
            return

        if not (cooldown := cooldowns.auto(m.author.id, command.kwargs['name'], command.kwargs['cooldown'])):
            await result
        else:
            if not cooldowns.auto(m.author.id, '_cooldown', 2):
                await m.send(embed=dispatch_errors.cooldown(cooldown))