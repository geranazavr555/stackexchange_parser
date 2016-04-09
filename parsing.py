"""
    Содержит инструменты, использующиеся при разборе xml.
"""
from time import time
import settings


def parse(raw_data):
    start_time = time()
    parsed_data = []
    raw_data = raw_data[2:-1]  # Обрезание xml-заголовка и <%filename%></%filename%>:
    for row in raw_data:
        parsed_data.append(parse_xml_line(row))
    if settings.debug:
        print('parse() time (sec):', time() - start_time)
    return parsed_data


def parse_xml_line(line):
    """
        Преобразует строку xml в словарь {поле : значение}
    """
    line = line.lstrip()[5:-3]  # Удаление пробельных символов в начале строки и обрезание <row ... />
    content = dict()
    start = 0  # start - позиция начала имени поля
    sep = 0  # sep - позиция разделителя поле/значение
    opened = False  # opened - открыты ли кавычки (Если да, значит текущее положение внутри значения)
    for i in range(len(line)):
        if line[i] == '=':
            sep = i
        elif line[i] == '"':
            if opened:
                opened = False
                content[line[start:sep]] = line[sep + 2:i]  # добавление поля и значения в ответ
                start = i + 2
            else:
                opened = True
    return content


def get_hour(datetime):
    """
        Выделяет из строки вида yyyy-mm-ddThh-mm-ss.sss часы
    """
    return int(datetime[datetime.find('T') + 1:datetime.find(':')])
