"""Модуль записи результатов выборки

Содержит инструменты для генерации результатов выборки в формате html

"""


class GenOutput:
    """Генератор html-отчета

    Генерирует html-страницу с результатами выборки

    """

    def __init__(self, _raw_output):
        """Инициализирует генератор, используя данные выборки"""

        # __raw_data - хранит данные для записи
        self.__raw_data = _raw_output

        # __page - хранит html-страницу
        self.__page = []

        # __stack - Хранит список ещё не закрытых html-тегов:
        self.__stack = []

        # Установка настроек по умолчанию
        self.settings = {
            'generate_css': False,
            'generate_header': False,
            'website': 'physics.stackexchange.com',
            'html_spaces': 2,
            'out_limit_type': 0,
            'html_output_file': 'results.html'
        }

    def generate(self):
        """Генерирует страницу"""

        self.__open_tag('html')
        self.__open_tag('head')

        # Явное указание кодировки
        self.__open_tag('meta', {'charset': 'utf-8'})
        self.__close_tag()

        if self.settings['generate_css']:
            # Генерирование оформления
            self.__gen_css()

        self.__close_tag()
        self.__open_tag('body')

        if self.settings['generate_header']:
            # Генерирование заголовка
            self.__gen_header()

        # Вызов генератора таблицы с результатами
        self.__gen_table()

        self.__close_tag()
        self.__close_tag()

    def __open_tag(self, tag, attributes=None):
        """Открывает html-tag"""

        # Если атрибутов нет - простой тег, иначе - генерация тега с атрибутами
        if attributes is None:
            line = '<' + tag + '>'
        else:
            line = '<' + tag
            for attribute in attributes:
                line += ' ' + attribute + '="' + attributes[attribute] + '"'
            line += '>'
        self.__writeln(line)
        self.__stack.append(tag)

    def __close_tag(self):
        """Закрывает последний открытый тег"""
        self.__writeln('</' + self.__stack.pop() + '>')

    def __gen_link(self, num):
        """Генерирует адрес ссылки на конкретного пользователя"""
        return 'http://' + self.settings['website'] + '/users/' + num

    def __writeln(self, line):
        """Записывает строку с отступами"""
        self.__page.append(' ' * len(self.__stack) * self.settings['html_spaces'] + line + '\n')

    def __gen_row(self, row, th_tag=False, user_id_pos=1):
        """Создаёт одну строку таблицы"""

        self.__open_tag('tr')
        for cell_i in range(len(row)):
            if th_tag:
                self.__open_tag('th')
            else:
                self.__open_tag('td')
            if cell_i == user_id_pos:
                # Если текущая ячейка - user_id, то сгенерировать ссылку на него
                self.__open_tag('a', {'href': self.__gen_link(row[cell_i]), 'target': '_blank'})
                self.__writeln(str(row[cell_i]))
                self.__close_tag()
            else:
                self.__writeln(str(row[cell_i]))
            self.__close_tag()
        self.__close_tag()

    def __gen_header(self):
        """Генерирование заголовка и дополнительной информации"""

        self.__open_tag('h1')
        self.__writeln('Результаты выборки')
        self.__close_tag()

        self.__open_tag('hr')
        self.__close_tag()

        self.__writeln('Для перехода к профилю пользователя на сайте ' + self.settings['website'] +
                       ' перейдите по ссылке, кликнув на идентификатор пользователя')
        self.__open_tag('br')
        self.__close_tag()
        self.__writeln('Всего найдено пользователей, имеющих хотя бы 1 подходящий пост: ' + str(len(self.__raw_data)))
        self.__open_tag('br')
        self.__close_tag()
        self.__writeln('Могут быть показаны не все пользователи, смотрите настройки составления отчёта')

        self.__open_tag('hr')
        self.__close_tag()

    def __gen_css(self):
        """Запись стилей"""

        style = GenStyle()
        style.gen_style('table', {'width': '35%', 'margin': 'auto'})
        style.gen_style('tr', {'background': 'rgba(165, 255, 235, 0.5)'})
        style.gen_style('th', {'background': 'rgba(165, 255, 235, 1)'})
        style.gen_style('tr:hover', {'background': 'rgba(165, 255, 235, 0.75)'})

        self.__open_tag('style', {'type': 'text/css'})
        self.__writeln(style.css)
        self.__close_tag()

    def __gen_table(self):
        """Запись таблицы с результатами выборки"""

        self.__open_tag('table', {'border': '1', 'rules': 'all', 'cellpadding': '3'})

        # Запись заголовка таблицы
        self.__gen_row(['#', 'User id', 'Posts count'], th_tag=True, user_id_pos=-1)

        i = 0
        for row in self.__raw_data:
            i += 1
            # Учитывание ограничений, заданных пользователем
            if self.settings['out_limit_type'] == 1:
                # Проверка ограничения на число пользователей
                if i > self.settings['out_limit']:
                    break
            elif self.settings['out_limit_type'] == 2:
                # Проверка мягкого ограничения на число пользователей
                if row[1] < self.__raw_data[self.settings['out_limit'] - 1][1]:
                    break
            elif self.settings['out_limit_type'] == 3:
                # Проверка количества постов
                if row[1] < self.settings['out_limit']:
                    break
            self.__gen_row([i, row[0], row[1]])

        self.__close_tag()

    def writefile(self, filename=None):
        """Запись страницы на диск"""
        if filename is None:
            filename = self.settings['html_output_file']
        file = open(filename, 'w', encoding='utf-8')
        file.writelines(self.__page)
        file.close()


class GenStyle:
    """Генератор оформления

    Генерирует готовое оформление таблицы в css-формате

    """

    def __init__(self):
        self.css = ''

    def gen_style(self, name, attributes):
        """Генерирует стиль name с параметрами attributes"""
        self.__open_style(name)
        self.__write_style(attributes)
        self.__close_style()

    def __open_style(self, stylename):
        self.css += stylename + ' {\n'

    def __close_style(self):
        self.css += '}\n'

    def __write_style(self, style):
        """Записывает блок атрибутов стиля"""
        for attribute in style:
            self.__gen_attribute(attribute, style[attribute])

    def __gen_attribute(self, name, value):
        """Записывает пару {Атрибут : Значение}"""
        self.css += name + ': ' + value + ';\n'
