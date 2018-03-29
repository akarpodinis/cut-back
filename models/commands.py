import locale
import re

from .errors import CommandNotMatchedError, CommandSyntaxInvalidError


class CommandParseResult(object):
    name = ''


class SaveParseResult(CommandParseResult):
    name = 'save'

    def __init__(self, amount, on_thing, for_thing):
        self.amount = round(float(amount), 2)
        self.on_thing = on_thing.lower()
        self.for_thing = for_thing.lower()

    def execute(self, table):
        # table.add_saved(self.saved)
        print(self)

    def __str__(self):
        return 'Great!  You saved {} for {} when you skipped {}.'.format(
            locale.currency(self.amount),
            self.for_thing.capitalize(),
            self.on_thing.capitalize(),
        )


# TODO: Add verb support for 'save' ($ save 2.56 on coffee for magic)
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
