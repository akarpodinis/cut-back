#! /usr/local/bin/python3
import argparse

from models.commands import SaveCommand
from models.errors import (
    CommandNotFoundError, CommandNotMatchedError, CommandSyntaxInvalidError, CommandValidationError,
    InputError
)
from models.table import Tables

commands = [
    SaveCommand()
]


def command_search(input):
    for command in commands:
        try:
            return command.is_valid(input)
        except CommandNotMatchedError:
            continue

    junk_name = input.split(' ')[0] or 'do what now'
    raise CommandNotFoundError(f'You want me to {junk_name}?')


# TODO: Add verb support for 'spend' ($ spend 5.00 on magic)
# TODO: Add verb support for 'export' ($ export filename.csv)
# TODO: Add verb support for 'reload' ($ reload)
#       to reload the file from disk to load direct changes while running program
# TODO: Change underlying data structure to be objects in memory instead of a list of dictionaries.
# TODO: Implement a scratchpad and ask to save?
# BUG: Currency ingenstion doesn't accept commas
# √: Refactor to not save 'skipped_thing'
# √: Add a summary of commands available at startup
# √: Add verb support for 'save' ($ save 2.56 on coffee for magic)
# √: Add a summary when starting up
# √: Add CLI option to specify tables json location
# √: Add a CLA for summary output only
def main(parsed_args):
    location = parsed_args.file
    tables = Tables(location)

    taking_input = True

    print(tables.summary())

    if parsed_args.summary:
        return

    print('Ready to save!')
    command_list_string = ', '.join(command.command_name for command in commands)
    print(f'You can {command_list_string} right now.')

    try:
        while taking_input:
            try:
                raw_input = input(':> ')

                try:
                    validation_result = command_search(raw_input)
                    validation_result.execute(tables)
                except CommandNotFoundError as e:
                    print(e)
                except CommandSyntaxInvalidError as e:
                    print(e)
                except CommandValidationError as e:
                    print(e)
            except InputError as e:
                if isinstance(e.__cause__, EOFError):
                    raise e.__cause__
                print()
                print(e)
                taking_input = False
    except KeyboardInterrupt:
        print()
    except EOFError:
        print()

    print(tables.summary())
    tables.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Track pocket change for budgeting!')

    parser.add_argument(
        '-f',
        '--file',
        type=str,
        default='saved.json',
        help='Database file location, in json format.'
    )

    parser.add_argument(
        '-s',
        '--summary',
        default=False,
        action='store_true',
        help='Print a summary and exit.'
    )

    args = parser.parse_args()
    main(args)
    print('Done!')
