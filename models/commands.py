import inspect
import locale
import re
import sys

from .errors import CommandNotMatchedError, CommandSyntaxInvalidError
from .table import TableAdjustment


class SummaryParseResult(object):
    name = 'summary'

    def __init__(self):
        pass

    def execute(self, table):
        print(table.summary())

    def __str__(self):
        return ''


class SummaryCommand(object):
    regex = r'(sum(?:mary)?)'
    command_name = 'summary'
    command_name_short = 'sum'
    help = 'To get a summary, use \'sum\' or \'summary\'.'

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

        return SummaryParseResult()


class SpendParseResult(object):
    name = 'spend'

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
    name = 'save'

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
