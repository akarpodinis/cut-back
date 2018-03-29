import json

from utils import locale


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

    def add_saved(self, saved):
        for thing in self.table['saved']:
            if saved.for_thing not in thing['name']:
                continue

            thing['amount'] += saved.amount

    def summary(self):
        finalized_output = []
        for thing in self.table['saved']:
            saved_caps = thing['name'].capitalize()
            amount = round(float(thing['amount']), 2)
            formatted_amount = locale.currency(amount)
            finalized_output.append(f" {saved_caps} has {formatted_amount} saved.")

        return '\r\n'.join(finalized_output)
