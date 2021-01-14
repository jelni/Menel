from asyncio import Task
from traceback import print_exc

from cliffs import (
    CallMatchFail,
    CommandDispatcher,
    MismatchedLiteralSuggestion,
    MismatchedParameterType,
    UnknownCommandError
)

from command_dispatcher import dispatch_errors
from functions.clean_content import clean_content
from functions.user_perms import user_perms
from objects.cooldowns import cooldowns
from objects.message import Message


async def dispatch(cliffs: CommandDispatcher, m: Message, prefix: str):
    try:
        result, command = cliffs.dispatch(m.content[len(prefix):], m=m, prefix=prefix)
    except MismatchedLiteralSuggestion as e:
        await m.error(dispatch_errors.mismatched_literal_suggestion(e))

    except MismatchedParameterType as e:
        await m.error(dispatch_errors.mismatched_parameter_type(e))

    except CallMatchFail as fail:
        ...
        # if 'name' in fail.command.kwargs:
        #     await send(m.channel, commands.other.help.get_help(fail.command.kwargs['name'], prefix))

    except UnknownCommandError:
        pass
    else:
        if not result:
            return

        if 'perms' in command.kwargs and user_perms(m) < command.kwargs['perms']:
            await m.error(dispatch_errors.missing_perms(command.kwargs['perms']), delete_after=5)
            Task(result).cancel()
            return

        if not (cooldown := cooldowns.auto(m.author.id, command.kwargs['name'], command.kwargs['cooldown'])):
            try:
                await result
            except Exception as e:
                print_exc()
                await m.error(f'An error occurred\n{clean_content(e)}')
        else:
            Task(result).cancel()
            if not cooldowns.auto(m.author.id, '_cooldown', 2):
                await m.error(dispatch_errors.cooldown(cooldown), delete_after=5)