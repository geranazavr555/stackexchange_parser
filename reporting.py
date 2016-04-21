"""Модуль записи результатов выборки

Содержит инструменты для генерации результатов выборки в формате html

"""

from settings import settings


def gen_html(filename, raw_data, site=settings['website']):
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
        file.write(' ' * len(stack) * settings['html_spaces'] + line + '\n')

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
    file = open(filename, 'w', encoding='utf-8')

    open_tag('html')
    open_tag('head')

    open_tag('meta', {'charset': 'utf-8'})
    close_tag()

    if settings['generate_css']:
        # Генерирование оформления
        open_tag('style', {'type': 'text/css'})
        writeln(gen_css())
        close_tag()
        close_tag()

    close_tag()
    open_tag('body')

    if settings['generate_header']:
        # Генерирование заголовка
        open_tag('h1')
        writeln('Результаты выборки')
        close_tag()

        open_tag('hr')
        close_tag()

        writeln('Для перехода к профилю пользователя на сайте ' + settings['website'] +
                ' перейдите по ссылке, кликнув на идентификатор пользователя')
        open_tag('br')
        close_tag()
        writeln('Всего найдено пользователей, имеющих хотя бы 1 подходящий пост: ' + str(len(raw_data)))
        open_tag('br')
        close_tag()
        writeln('Могут быть показаны не все пользователи, смотрите настройки составления отчёта')

        open_tag('hr')
        close_tag()

    open_tag('table', {'border': '1', 'rules': 'all', 'cellpadding': '3'})

    gen_row(['#', 'User id', 'Posts count'], th_tag=True, user_id_pos=-1)
    i = 0
    for row in raw_data:
        i += 1
        # Учитывание ограничений, заданных пользователем
        if settings['out_limit_type'] == 1:
            # Проверка ограничения на число пользователей
            if i > settings['out_limit']:
                break
        elif settings['out_limit_type'] == 2:
            # Проверка мягкого ограничения на число пользователей
            if row[1] < raw_data[settings['out_limit'] - 1][1]:
                break
        elif settings['out_limit_type'] == 3:
            # Проверка количества постов
            if row[1] < settings['out_limit']:
                break
        gen_row([i, row[0], row[1]])

    # закрытие оставшихся тегов:
    while len(stack) > 0:
        close_tag()

    file.close()

css = ''


def gen_css():
    """Генератор оформления

    Генерирует готовое оформление таблицы в css-формате

    """

    def open_style(stylename):
        global css
        css += stylename + ' {\n'

    def close_style():
        global css
        css += '}\n'

    def write_style(style):
        """Записывает блок атрибутов стиля"""
        for attribute in style:
            gen_attribute(attribute, style[attribute])

    def gen_attribute(name, value):
        """Записывает пару {Атрибут : Значение}"""
        global css
        css += ' ' * settings['html_spaces'] + name + ': ' + value + ';\n'

    def gen_style(name, attributes):
        """Записывает один полный стиль"""
        global css
        css += ''
        open_style(name)
        write_style(attributes)
        close_style()

    global css

    gen_style('table', {'width': '35%', 'margin': 'auto'})
    gen_style('tr', {'background': 'rgba(165, 255, 235, 0.5)'})
    gen_style('th', {'background': 'rgba(165, 255, 235, 1)'})
    gen_style('tr:hover', {'background': 'rgba(165, 255, 235, 0.75)'})

    return css
