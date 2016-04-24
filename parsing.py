"""Модуль парсинга

Содержит инструменты, использующиеся при разборе xml.

"""


def parse(raw_data):
    """Преобразует список xml-строк в список словарей {ключ:значение}"""

    parsed_data = []

    # Обрезание xml-заголовка и <%filename%></%filename%>:
    raw_data = raw_data[2:-1]

    for row in raw_data:
        parsed_data.append(parse_xml_line(row))

    return parsed_data


def parse_xml_line(line):

    """Преобразует строку xml в словарь {поле : значение}"""
    # Удаление пробельных символов в начале строки и обрезание <row ... />
    line = line.lstrip()
    line = line[5:-3]

    content = dict()

    # start - позиция начала имени поля
    start = 0
    # sep - позиция разделителя поле/значение
    sep = 0
    # opened - открыты ли кавычки (Если да, значит текущее положение внутри значения)
    opened = False

    for i in range(len(line)):
        if line[i] == '=':
            sep = i
        elif line[i] == '"':
            if opened:
                opened = False
                # добавление поля и значения в ответ:
                content[line[start:sep]] = line[sep + 2:i]
                start = i + 2
            else:
                opened = True
    return content
