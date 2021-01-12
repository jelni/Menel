from cliffs import (
    CallMatchFail,
    CommandDispatcher,
    MismatchedLiteralSuggestion,
    MismatchedParameterType,
    UnknownCommandError
)

from command_dispatcher import dispatch_errors
from objects.message import Message


async def dispatch(cliffs: CommandDispatcher, m: Message, prefix: str):
    try:
        result, kwargs = cliffs.dispatch(m.content[len(prefix):], m=m, prefix=prefix)
    except MismatchedLiteralSuggestion as e:
        await m.send(dispatch_errors.mismatched_literal_suggestion(e))

    except MismatchedParameterType as e:
        await m.send(dispatch_errors.mismatched_parameter_type(e))

    except CallMatchFail as fail:
        ...
        # if 'name' in fail.command.kwargs:
        #     await send(m.channel, commands.other.help.get_help(fail.command.kwargs['name'], prefix))

    except UnknownCommandError:
        pass
    else:
        if not result:
            return

        await result