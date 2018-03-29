class InputError(Exception):
    pass


class CommandValidationError(Exception):
    pass


class CommandNotFoundError(Exception):
    pass


class CommandNotMatchedError(Exception):
    pass


class CommandSyntaxInvalidError(Exception):
    pass


class TableItemLessThanZeroError(Exception):
    pass


class TableItemNotFoundError(Exception):
    pass
