#! /usr/local/bin/python3
import argparse

from models.tables import Saved, Tables
from models.errors import InputError


# TODO: Add verb support for 'save' ($ save 2.56 on coffee for magic)
# TODO: Add verb support for 'spend' ($ spend 5.00 on magic)
# TODO: Add verb support for 'export' ($ export filename.csv)
# TODO: Add verb support for 'reload' ($ reload)
#       to reload the file from disk to load direct changes while running program
# TODO: Refactor to not save 'skipped_thing'
# TODO: Change underlying data structure to be objects in memory instead of a list of dictionaries.
# TODO: Implement a scratchpad and ask to save?
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

    try:
        while taking_input:
            try:
                saved = Saved.prompt()
                if saved:
                    tables.add_saved(saved)
                    print(saved.summary())
                else:
                    taking_input = False
            except InputError as e:
                if isinstance(e.__cause__, EOFError):
                    raise e.__cause__
                print()
                print(e)
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
