import importlib
import pkgutil

from cliffs import CommandDispatcher

from Menel import commands


# Inspired by https://github.com/python-discord/bot/blob/master/bot/utils/extensions.py


def import_commands(cliffs: CommandDispatcher):
    imported = set()
    skipped = set()

    for module in pkgutil.walk_packages(commands.__path__, commands.__name__ + '.'):
        if module.name.rsplit('.', maxsplit=1)[-1].startswith('_'):
            continue

        module = importlib.import_module(module.name)
        if hasattr(module, 'setup'):
            module.setup(cliffs)
            imported.add(module.__name__)
        else:
            skipped.add(module.__name__)

    print(f'Imported {", ".join(imported)}')
    if skipped:
        print(f'Skipped {", ".join(skipped)}')