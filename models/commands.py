import inspect
import locale
import re
import sys

from .errors import CommandNotMatchedError, CommandSyntaxInvalidError
from .table import TableAdjustment

"""
Don't forget, you can add classes that end in `...Command` and have them automatically
detected and loaded by the command validator.

`...ParseResult` should implement __init__(), execute(), __str__() and audit().
`...Command` should implement is_valid() and have properties regex, command_name and help.
"""


class RemoveParseResult(object):
    def __init__(self, name):
        self.name = name

    def execute(self, table):
        removed = table.remove(self.name)
        self.amount = removed['amount']
        print(self)

    def __str__(self):
        return 'You removed {} saved for {}.'.format(
            locale.currency(self.amount),
            self.name.capitalize()
        )

    def audit(self, separator='\t'):
        return f'remove{separator}{self.amount}{separator}{self.name}'


class RemoveCommand(object):
    regex = r'(remove) ([\w ]*)'
    command_name = 'remove'
    help = 'To remove, use \'remove thing\'.'

    def is_valid(self, input_string):
        pattern = re.compile(self.regex)
        matches = pattern.match(input_string)
        if not matches:
            if self.command_name in input_string:
                raise CommandSyntaxInvalidError(self.help)
            else:
                raise CommandNotMatchedError()

        if self.command_name not in matches.group(1) or pattern.groups != 2:
            raise CommandSyntaxInvalidError(self.help)

        return RemoveParseResult(matches.group(2))


class TransferParseResult(object):
    def __init__(self, amount, from_thing, to_thing):
        self.amount = abs(round(float(amount), 2))
        self.from_thing = from_thing
        self.to_thing = to_thing

    def execute(self, table):
        table.adjust_table(TableAdjustment(self.from_thing, self.amount * -1))
        table.adjust_table(TableAdjustment(self.to_thing, self.amount))
        print(self)

    def __str__(self):
        return 'You transferred {} from {} to {}.'.format(
            locale.currency(self.amount),
            self.from_thing.capitalize(),
            self.to_thing.capitalize()
        )

    def audit(self, sep='\t'):
        return f'transfer{sep}{self.amount}{sep}{self.from_thing}{sep}{self.to_thing}'


class TransferCommand(object):
    regex = r'(transfer) \$?([\d,]*\.?\d*) from ([\w ]*) to ([\w ]*)'
    command_name = 'transfer'
    help = 'To transfer, use \'transfer $0.00 from thing to other_thing\'.'

    def is_valid(self, input_string):
        pattern = re.compile(self.regex)
        matches = pattern.match(input_string)
        if not matches:
            if self.command_name in input_string:
                raise CommandSyntaxInvalidError(self.help)
            else:
                raise CommandNotMatchedError()

        if self.command_name not in matches.group(1) or pattern.groups != 4:
            raise CommandSyntaxInvalidError(self.help)

        return TransferParseResult(matches.group(2), matches.group(3), matches.group(4))


class SummarizeParseResult(object):
    name = 'summarize'

    def __init__(self):
        pass

    def execute(self, table):
        print(table.summary())

    def __str__(self):
        return ''

    def audit(self, separator='\t'):
        return 'summarize'


class SummarizeCommand(object):
    regex = r'(sum(?:marize)?)'
    command_name = 'summarize'
    command_name_short = 'sum'
    help = 'To summarize, use \'sum\' or \'summarize\'.'

    def is_valid(self, input_string):
        pattern = re.compile(self.regex)
        matches = pattern.match(input_string)
        if not matches:
            if self.command_name in input_string:
                raise CommandSyntaxInvalidError(self.help)
            else:
                raise CommandNotMatchedError()

        if self.command_name_short not in matches.group(1) or pattern.groups != 1:
            raise CommandSyntaxInvalidError(self.help)

        return SummarizeParseResult()


class SpendParseResult(object):
    def __init__(self, amount, for_thing):
        self.for_thing = for_thing
        self.amount = abs(round(float(amount), 2))

    def execute(self, table):
        table.adjust_table(TableAdjustment(self.for_thing, self.amount * -1))
        print(self)

    def __str__(self):
        return 'Hard work pays off!  You spent {} on {}.'.format(
            locale.currency(self.amount),
            self.for_thing.capitalize(),
        )

    def audit(self, separator='\t'):
        return f'spend{separator}{self.amount}{separator}{self.for_thing}'


class SpendCommand(object):
    regex = r'(spend) \$?([\d,]*\.?\d*) on ([\w ]*)'
    command_name = 'spend'
    help = 'To spend, use \'spend $0.00 on thing\'.  Positive numbers only!'

    def is_valid(self, input_string):
        pattern = re.compile(self.regex)
        matches = pattern.match(input_string)
        if not matches:
            if self.command_name in input_string:
                raise CommandSyntaxInvalidError(self.help)
            else:
                raise CommandNotMatchedError()

        if self.command_name not in matches.group(1) or pattern.groups != 3:
            raise CommandSyntaxInvalidError(self.help)

        return SpendParseResult(matches.group(2), matches.group(3))


class SaveParseResult(object):
    def __init__(self, amount, on_thing, for_thing):
        self.amount = round(float(amount), 2)
        self.on_thing = on_thing.lower()
        self.for_thing = for_thing.lower()

    def execute(self, table):
        table.adjust_table(TableAdjustment(self.for_thing, self.amount))
        print(self)

    def __str__(self):
        return 'Great!  You saved {} for {} when you skipped {}.'.format(
            locale.currency(self.amount),
            self.for_thing.capitalize(),
            self.on_thing.capitalize(),
        )

    # `sep` means `separator`.  I hate abbreviations but I hate over-run line lenghts more.
    def audit(self, sep='\t'):
        return f'save{sep}{self.amount}{sep}{self.on_thing}{sep}{self.for_thing}'


class SaveCommand(object):
    regex = r'(save) \$?([\d,]*\.?\d*) on ([\w ]*) for ([\w ]*)'
    command_name = 'save'
    help = 'To save, use \'save $0.00 on thing for other_thing\'.'

    def is_valid(self, input_string):
        pattern = re.compile(self.regex)
        matches = pattern.match(input_string)
        if not matches:
            if self.command_name in input_string:
                raise CommandSyntaxInvalidError(self.help)
            else:
                raise CommandNotMatchedError()

        if self.command_name not in matches.group(1) or pattern.groups != 4:
            raise CommandSyntaxInvalidError(self.help)

        return SaveParseResult(matches.group(2), matches.group(3), matches.group(4))


def all_commands():
    commands = list(map(
        lambda cls: cls[1](),
        filter(
            lambda cls: cls[0].endswith('Command'),
            inspect.getmembers(sys.modules[__name__], inspect.isclass)
        )
    ))

    return commands
