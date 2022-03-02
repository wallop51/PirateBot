from json import dumps, loads

class EnvironmentContainer:
    def __init__(self, filename='.env', required=()):
        try:
            with open(filename) as file:
                variables = loads(file.read())

            for key, value in variables.items():
                self.__setattr__(key, value)
        except FileNotFoundError():
            for key in required:
                value = input(f'Enter {key}: ')
                self.__setattr__(key, value)
        except Exception as e:
            raise e
