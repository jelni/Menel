from random import choice


def setup(cliffs):
    @cliffs.command('dywan [<width: int>] [<length: int>]', name='dywan', cooldown=3)
    async def command_dywan(m, width=15, length=10):
        if width <= 0 or length <= 0:
            await m.error('Taki dywan byłby za mały, kasztanie')
            return

        if width > 25 or length > 100 or width * length > 2000:
            await m.error('Taki dywan byłby za szeroki, kasztanie!')
            return

        lines = list()
        for _ in range(length):
            line = str()
            for _ in range(width):
                line += choice('╱╲')

            lines.append(f'┃{line}┃')

        line = '━' * width
        lines.insert(0, f'┏{line}┓')
        lines.append(f'┗{line}┛')

        lines = '```\n' + '\n'.join(lines) + '\n```'

        await m.success(f'Proszę, oto Twój darmowy dywan\n{lines}')