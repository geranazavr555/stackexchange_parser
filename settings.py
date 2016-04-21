"""Файл настроек"""


def read_strings_from_file(filename):
    file = open(filename, 'r')
    raw_list = file.readlines()
    file.close()
    return raw_list


class Settings:
    def __init__(self):
        self.data = {}
        self.load_from_file()

    def load_from_file(self, filename='default.cfg'):
        raw = read_strings_from_file(filename)
        for line in raw:
            if line.startswith('#') or line.startswith('\n'):
                continue
            key, value = line.split(' = ')
            self.data[key] = value

    def clear(self):
        self.data.clear()

settings = Settings()
