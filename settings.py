"""Файл настроек"""


class Settings:
    def __init__(self):
        self.data = {}
        self.load_defaults()
        self.load_from_file()

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        return self.data.__str__()

    def load_defaults(self):

        self.data['min_reputation'] = -10 ** 18
        self.data['max_reputation'] = 10 ** 18

        self.data['min_hour'] = 0
        self.data['max_hour'] = 24

    def load_from_file(self, filename='default.cfg'):

        file = open(filename, 'r', encoding='utf-8')
        raw = file.readlines()
        file.close()

        for line in raw:
            if line.startswith('#') or line.startswith('\n'):
                continue
            key, value = line.split(' = ')
            self.data[key] = value.rstrip('\n')

        self.repare_types()

    def repare_types(self):

        int_keys = {
            'html_spaces',
            'out_limit_type',
            'out_limit',
            'min_reputation',
            'max_reputation',
            'min_hour',
            'max_hour'
        }

        bool_keys = {
            'generate_css',
            'generate_header',
            'filter_accepted',
            'debug'
        }

        for key in self.data:
            if key in int_keys:
                self.data[key] = int(self.data[key])
            elif key in bool_keys:
                self.data[key] = bool(int(self.data[key]))

    def clear(self):
        self.data.clear()
        self.load_defaults()

settings = Settings()

if settings['debug']:
    print(settings)
