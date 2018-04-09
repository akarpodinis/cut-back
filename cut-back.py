#! /usr/local/bin/python3
import argparse

from models.audit_log import AuditLog
from models.commands import all_commands
from models.errors import (
    CommandNotFoundError, CommandNotMatchedError, CommandSyntaxInvalidError, CommandValidationError,
    InputError, TableItemLessThanZeroError, TableItemNotFoundError
)
from models.table import Tables

commands = all_commands()


def command_search(input):
    for command in commands:
        try:
            return command.is_valid(input)
        except CommandNotMatchedError:
            continue

    junk_name = input.split(' ')[0] or 'do what now'
    raise CommandNotFoundError(f'You want me to {junk_name}?')


# TODO: Change underlying data structure to be objects in memory instead of a list of dictionaries.
# TODO: Implement a scratchpad and ask to save?
# √: Add an audit log saved to the local directory
# √: Add verb support to 'remove' tracking for an item outright ($ remove thing)
# √: Add verb support to 'transfer' from one to another ($ transfer $0.00 from thing to thing)
# √: Add verb support for `summary` ($ summary)
# √: Generalize command class loading
# √: Add verb support for 'spend' ($ spend 5.00 on magic)
# √: Refactor to not save 'skipped_thing'
# √: Add a summary of commands available at startup
# √: Add verb support for 'save' ($ save 2.56 on coffee for magic)
# √: Add a summary when starting up
# √: Add CLI option to specify tables json location
# √: Add a CLA for summary output only
# x: Add verb support for 'export' ($ export filename.csv)
#    This has been supplanted by audit logging
def main(parsed_args):
    table_location = parsed_args.file
    tables = Tables(table_location)

    audit_location = parsed_args.audit_file
    audit_log = AuditLog(audit_location)

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
                    audit_log.log(validation_result)
                except CommandNotFoundError as e:
                    print(e)
                except CommandSyntaxInvalidError as e:
                    print(e)
                except CommandValidationError as e:
                    print(e)
                except TableItemLessThanZeroError as e:
                    print(e)
                except TableItemNotFoundError as e:
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
    audit_log.close()


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

    parser.add_argument(
        '-a',
        '--audit_file',
        default='log.tsv',
        help='Audit log output file location, tab-separated. A file will be created if none exists.'
    )

    parser.add_argument(
        '--no_audit',
        default=False,
        action='store_true',
        help='Turns off auditing.  Defaults to auditing on.'
    )

    args = parser.parse_args()
    main(args)
    print('Done!')
