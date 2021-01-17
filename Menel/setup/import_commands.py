import importlib
import pkgutil

from cliffs import CommandDispatcher

from Menel import commands


COMMANDS = dict()


# Inspired by https://github.com/python-discord/bot/blob/master/bot/utils/extensions.py

def unqualify(name: str) -> str:
    return name.rsplit('.', maxsplit=1)[-1]


def import_commands(cliffs: CommandDispatcher):
    imported = set()
    skipped = set()

    for module in pkgutil.walk_packages(commands.__path__, commands.__name__ + '.'):
        if unqualify(module.name).startswith('_'):
            continue

        module = importlib.import_module(module.name)
        name = unqualify(module.__name__)
        if hasattr(module, 'setup'):
            module.setup(cliffs)
            imported.add(name)
        else:
            skipped.add(name)

    print(f'Imported {", ".join(imported)}')
    if skipped:
        print(f'Skipped {", ".join(skipped)}')