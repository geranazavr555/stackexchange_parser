"""Модуль записи результатов выборки

Содержит инструменты для генерации результатов выборки в формате html

"""

from settings import settings


class GenOutput:

    def __init__(self, _raw_output):

        self.raw_data = _raw_output

        self.page = []

        # stack - Хранит список ещё не закрытых html-тегов:
        self.stack = []

        self.__open_tag('html')
        self.__open_tag('head')

        self.__open_tag('meta', {'charset': 'utf-8'})
        self.__close_tag()

        if settings['generate_css']:
            # Генерирование оформления
            style = GenStyle()
            style.gen_style('table', {'width': '35%', 'margin': 'auto'})
            style.gen_style('tr', {'background': 'rgba(165, 255, 235, 0.5)'})
            style.gen_style('th', {'background': 'rgba(165, 255, 235, 1)'})
            style.gen_style('tr:hover', {'background': 'rgba(165, 255, 235, 0.75)'})

            self.__open_tag('style', {'type': 'text/css'})
            self.__writeln(style.css)
            self.__close_tag()

        self.__close_tag()
        self.__open_tag('body')

        if settings['generate_header']:
            # Генерирование заголовка
            self.__open_tag('h1')
            self.__writeln('Результаты выборки')
            self.__close_tag()

            self.__open_tag('hr')
            self.__close_tag()

            self.__writeln('Для перехода к профилю пользователя на сайте ' + settings['website'] +
                           ' перейдите по ссылке, кликнув на идентификатор пользователя')
            self.__open_tag('br')
            self.__close_tag()
            self.__writeln('Всего найдено пользователей, имеющих хотя бы 1 подходящий пост: ' + str(len(self.raw_data)))
            self.__open_tag('br')
            self.__close_tag()
            self.__writeln('Могут быть показаны не все пользователи, смотрите настройки составления отчёта')

            self.__open_tag('hr')
            self.__close_tag()

        self.__open_tag('table', {'border': '1', 'rules': 'all', 'cellpadding': '3'})

        self.__gen_row(['#', 'User id', 'Posts count'], th_tag=True, user_id_pos=-1)
        i = 0
        for row in self.raw_data:
            i += 1
            # Учитывание ограничений, заданных пользователем
            if settings['out_limit_type'] == 1:
                # Проверка ограничения на число пользователей
                if i > settings['out_limit']:
                    break
            elif settings['out_limit_type'] == 2:
                # Проверка мягкого ограничения на число пользователей
                if row[1] < self.raw_data[settings['out_limit'] - 1][1]:
                    break
            elif settings['out_limit_type'] == 3:
                # Проверка количества постов
                if row[1] < settings['out_limit']:
                    break
            self.__gen_row([i, row[0], row[1]])

        # закрытие оставшихся тегов:
        while len(self.stack) > 0:
            self.__close_tag()

    def __open_tag(self, tag, attributes=None):
        # Если атрибутов нет - простой тег, иначе - генерация тега с атрибутами
        if attributes is None:
            line = '<' + tag + '>'
        else:
            line = '<' + tag
            for attribute in attributes:
                line += ' ' + attribute + '="' + attributes[attribute] + '"'
            line += '>'
        self.__writeln(line)
        self.stack.append(tag)

    def __close_tag(self):
        self.__writeln('</' + self.stack.pop() + '>')

    @staticmethod
    def __gen_link(num, type_='users', website=settings['website']):
        """Генерирует адрес ресурса

        type_ - тип ресурса, по умолчанию = users
        num - номер ресураа

        """
        return 'http://' + website + '/' + type_ + '/' + num

    def __writeln(self, line):
        """Записывает строку с отступами в выходной файл"""
        self.page.append(' ' * len(self.stack) * settings['html_spaces'] + line + '\n')

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

    def writefile(self, filename=settings['html_output_file']):
        file = open(filename, 'w', encoding='utf-8')
        file.writelines(self.page)
        file.close()


class GenStyle:
    """Генератор оформления

    Генерирует готовое оформление таблицы в css-формате

    """
    def __init__(self):
        self.css = ''

    def gen_style(self, name, attributes):
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
        self.css += ' ' * settings['html_spaces'] + name + ': ' + value + ';\n'
