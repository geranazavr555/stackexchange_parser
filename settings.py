"""Модуль настроек

Модуль содержит класс Settings, отвечающий за настройки программы
и инициализирует их.
Зависит от reading.py

"""

from reading import read_raw_file


class Settings:
    """Класс настроек"""

    def __init__(self):
        self.data = {}
        self.load_defaults()
        self.load_from_file()

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        return self.data.__str__()

    def load_defaults(self):
        """Заполнение значений по умолчанию"""

        self.data['min_reputation'] = -10 ** 18
        self.data['max_reputation'] = 10 ** 18
        self.data['min_hour'] = 0
        self.data['max_hour'] = 24

        self.data['debug'] = False
        self.data['out_limit_type'] = 0
        self.data['generate_css'] = False
        self.data['generate_header'] = False
        self.data['html_spaces'] = 2
        self.data['html_output_file'] = ''

    def validate(self):
        """Проверяет правильность настроек.
        При наличии ошибки выводит её описание в stdout.
        Возвращвет, правильно ли заполнены настройки. (True/False)
        """

        keys = {
            'users_file_name',
            'posts_file_name',
            'post_type',
            'website'
        }
        for key in keys:
            if key not in self.data:
                print('Не заполнено поле ' + key)
                return False

        if self.data['out_limit_type'] > 0 and 'out_limit' not in self.data:
            print('Указан тип ограничения на вывод, но не указано его значение.')
            print('Не заполнено поле out_limit')
            return False

        if self.data['post_type'] == '2' and 'filter_accepted' not in self.data:
            print('Не заполнено поле filter_accepted')
            return False

        return True

    def load_from_file(self, filename='default.cfg'):
        """Считывание файла настроек из filename"""

        try:
            raw = read_raw_file(filename)
        except IOError:
            # Если произошла ошибка, то файла не существует. Возможно, так и задумано.
            pass
        else:
            for line in raw:
                if line.startswith('#') or line.startswith('\n'):
                    continue
                key, value = line.split(' = ')
                self.data[key] = value.rstrip('\n')
        finally:
            self.repair_types()

    def repair_types(self):
        """Явное приведение типов отдельных полей
        Метод приводит типы полей от str() к необходимому
        """

        # Целочисленные поля
        int_keys = {
            'html_spaces',
            'out_limit_type',
            'out_limit',
            'min_reputation',
            'max_reputation',
            'min_hour',
            'max_hour'
        }

        # Булевы поля
        bool_keys = {
            'generate_css',
            'generate_header',
            'filter_accepted',
            'debug'
        }

        # Приведение типов
        for key in self.data:
            if key in int_keys:
                self.data[key] = int(self.data[key])
            elif key in bool_keys:
                self.data[key] = bool(int(self.data[key]))

    def clear(self):
        """Сброс настроек"""
        self.data.clear()
        self.load_defaults()

settings = Settings()
