from datetime import datetime


# Class clustering for fun and profit!
class AuditLog(object):
    def __new__(cls, filepath):
        if filepath:
            return DefaultAuditLog(filepath)
        else:
            return EmptyAuditLog()


class DefaultAuditLog(object):
    def __init__(self, filepath):
        self.file = open(filepath, 'a')

    def log(self, parse_response):
        print(f'{datetime.now()}\t{parse_response.audit()}', file=self.file, flush=True)

    def close(self):
        self.file.close()


class EmptyAuditLog(object):
    def __init__(self):
        pass

    def log(self, parse_response):
        pass

    def close(self):
        pass
