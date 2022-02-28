from json import dumps, loads

class EnvironmentContainer:
    def __init__(self, filename='.env'):
        with open(filename) as file:
            variables = loads(file.read())

        for key, value in variables.items():
            self.__setattr__(key, value)
