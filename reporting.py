"""Модуль записи результатов выборки

Содержит инструменты для генерации результатов выборки в формате html

"""

import settings


def gen_html(filename, raw_data, encoding_=settings.out_encoding, site=settings.website):
    """Записывает html-страницу с результатами в %filename%"""

    def open_tag(tag, attributes=None):
        # Если атрибутов нет - простой тег, иначе - генерация тега с атрибутами
        if attributes is None:
            line = '<' + tag + '>'
        else:
            line = '<' + tag
            for attribute in attributes:
                line += ' ' + attribute + '="' + attributes[attribute] + '"'
            line += '>'
        writeln(line)
        stack.append(tag)

    def close_tag():
        writeln('</' + stack.pop() + '>')

    def gen_link(num, type_='users', website=site):
        """Генерирует адрес ресурса

        type_ - тип ресурса, по умолчанию = users
        num - номер ресураа

        """
        return 'http://' + website + '/' + type_ + '/' + num

    def writeln(line):
        """Записывает строку с отступами в выходной файл"""
        file.write(' ' * len(stack) * settings.html_spaces + line + '\n')

    def gen_row(row, th_tag=False, user_id_pos=1):
        """Создаёт и записывает одну строку таблицы"""

        open_tag('tr')
        for cell_i in range(len(row)):
            if th_tag:
                open_tag('th')
            else:
                open_tag('td')
            if cell_i == user_id_pos:
                # Если текущая ячейка - user_id, то сгенерировать ссылку на него
                open_tag('a', {'href': gen_link(row[cell_i]), 'target': '_blank'})
                writeln(str(row[cell_i]))
                close_tag()
            else:
                writeln(str(row[cell_i]))
            close_tag()
        close_tag()

    # stack - Хранит список ещё не закрытых html-тегов:
    stack = []
    file = open(filename, 'w', encoding=encoding_)

    open_tag('html')
    open_tag('body')
    open_tag('table')

    gen_row(['#', 'User id', 'Posts count'], th_tag=True)
    i = 0
    for row in raw_data:
        i += 1
        gen_row([i, row[0], row[1]])

    # закрытие оставшихся тегов:
    while len(stack) > 0:
        close_tag()

    file.close()
