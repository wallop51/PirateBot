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

class LangContatiner:
    class SubContainer:
        def __init__(self, data):
            self.data = data
        def exists(self, name):
            return bool(name in self.data)
        def update(self, dictionary):
            self.data.update(dictionary)
        def __getattr__(self, name):
            return self.data[name]
        def __getitem__(self, name):
            return self.data[name]

    def __init__(self, locale='en_GB.lang'):
        if not locale:
            import locale, ctypes
            locale = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()] + '.lang'

        self.locale = locale
        self.data = {}
        try:
            with open(locale) as file:
                lines = file.readlines()
        except FileNotFoundError:
            pass
        except Exception as e:
            raise e

        for line in lines:
            if line.find('#') != -1:
                line = line[:line.index('#')]
            if line.strip() == '':
                continue

            key = line[:line.index('=')]
            value = line[line.index('=')+1:].rstrip()
            parts = key.split('.')

            current = self.data
            for i in range(len(parts)):
                part = parts[i]
                if i+1 < len(parts): next_part = parts[i+1]

                try:
                    current = current[part]
                except:
                    needs_creating = parts[i:]
                    needs_creating.reverse()
                    curr = value
                    for p in needs_creating[:-1]:
                        curr = self.SubContainer({p:curr})
                    current.update({needs_creating[-1]: curr})

    def __getattr__(self, name):
        return self.data[name]