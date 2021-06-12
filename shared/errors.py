class IncorrectDataRecivedError(Exception):
    def __str__(self):
        return 'Invalid message received from remote computer.'

class ServerError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

class NonDictInputError(Exception):
    def __str__(self):
        return 'The argument of the function must be a dictionary.'

class ReqFieldMissingError(Exception):
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'The accepted dictionary is missing a required field {self.missing_field}.'