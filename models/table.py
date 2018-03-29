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
        self.table['saved'].append(vars(saved))

    def summary(self):
        saved_alike = {}
        for saved in self.table['saved']:
            saved_alike[saved['for_thing']] = []

        for saved in self.table['saved']:
            saved_alike[saved['for_thing']].append(saved)

        finalized_output = []

        for saved_for in saved_alike:
            total = 0
            for saved in saved_alike[saved_for]:
                total += round(float(saved['amount']), 2)
            saved_caps = saved['for_thing'].capitalize()
            formatted_amount = locale.currency(total)
            finalized_output.append(f" {saved_caps} has {formatted_amount} saved.")

        return '\r\n'.join(finalized_output)
