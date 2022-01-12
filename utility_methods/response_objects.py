import json


class Inn:
    def __init__(self, inn, errors):
        self.inn = inn
        self.errors = errors

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Suspension:
    def __init__(self, zip, mark, errors):
        self.zip = zip
        self.mark = mark
        self.errors = errors

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
