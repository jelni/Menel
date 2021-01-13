import os
import re
from importlib import import_module

from cliffs import CommandDispatcher


def import_commands(cliffs: CommandDispatcher):
    imported = set()
    skipped = set()

    for root, _, files in os.walk('commands'):
        for file in files:
            if not file.endswith('.py') or file.startswith('_'):
                continue

            module = import_module(re.sub(r'[/\\]', '.', os.path.join(root, file).removesuffix('.py')))
            if hasattr(module, 'setup'):
                module.setup(cliffs)
                imported.add(module.__name__)
            else:
                skipped.add(module.__name__)

    print(f'Imported {", ".join(imported)}')
    if skipped:
        print(f'Skipped {", ".join(skipped)}')