import json

from .errors import TableItemLessThanZeroError, TableItemNotFoundError
from utils import locale


class TableAdjustment(object):
    name = ''
    amount = 0.0

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class Tables(object):
    def __init__(self, path):
        self.path = path
        self.reload()

    def load(self):
        try:
            with open(self.path, 'r') as file_json:
                self.table = json.load(file_json)
        except Exception as e:
            print(f'Making a new file at {self.path}.')
            self.table = {
                'saved': []
            }

    def reload(self):
        self.load()
        self.save()

    def save(self):
        with open(self.path, 'w') as out:
            json.dump(self.table, out, indent=2)

    def remove(self, name):
        for thing in self.table['saved']:
            if thing['name'] == name:
                self.table['saved'].remove(thing)
                return thing

        raise TableItemNotFoundError('You can\'t remove something that doesn\'t exist!')

    def adjust_table(self, adjustment):
        actually_saved_something = False
        for thing in self.table['saved']:
            if adjustment.name != thing['name']:
                continue

            if thing['amount'] + adjustment.amount < 0:
                raise TableItemLessThanZeroError(
                    'You can\'t spend more on {} than you have!\r\n You have saved {}.'.format(
                        thing['name'],
                        locale.currency(round(float(thing['amount']), 2))
                    )
                )

            thing['amount'] += adjustment.amount
            actually_saved_something = True

        if not actually_saved_something:
            self.table['saved'].append({
                'name': adjustment.name,
                'amount': adjustment.amount
            })

    def summary(self):
        finalized_output = []
        for thing in self.table['saved']:
            saved_caps = thing['name'].capitalize()
            amount = round(float(thing['amount']), 2)
            formatted_amount = locale.currency(amount)
            finalized_output.append(f" {saved_caps} has {formatted_amount} saved.")

        return '\r\n'.join(finalized_output)
