"""Модуль записи результатов выборки

Содержит инструменты для генерации результатов выборки в формате html

"""

import settings


def gen_html(filename, raw_data, encoding_=settings.out_encoding):
    """Записывает html-страницу с результатами в %filename%"""

    def open_tag(tag):
        file.write(' ' * len(stack) * settings.html_spaces + '<' + tag + '>\n')
        stack.append(tag)

    def close_tag():
        file.write(' ' * (len(stack) - 1) * settings.html_spaces + '</' + stack.pop() + '>\n')

    def gen_row(row, th_tag=False):
        """Создаёт и записывает одну строку таблицы"""

        open_tag('tr')
        for cell in row:
            if th_tag:
                open_tag('th')
            else:
                open_tag('td')
            file.write(' ' * len(stack) * settings.html_spaces + str(cell) + '\n')
            close_tag()
        close_tag()

    # stack - Хранит список ещё не закрытых html-тегов:
    stack = []
    file = open(filename, 'w', encoding=encoding_)

    open_tag('html')
    open_tag('body')
    open_tag('table')

    gen_row(['#', 'UserID', 'Posts'], th_tag=True)
    i = 0
    for user_id in raw_data:
        i += 1
        gen_row([i, user_id, raw_data[user_id]])

    # закрытие оставшихся тегов:
    while len(stack) > 0:
        close_tag()

    file.close()
