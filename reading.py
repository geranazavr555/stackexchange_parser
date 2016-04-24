"""Модуль, содержащий инструменты для считывания"""


def read_raw_file(filename, encoding_='utf-8'):
    """Читает %filename% в кодировке %_encoding% и возвращает список строк"""

    file = open(filename, encoding=encoding_)
    raw_list = file.readlines()
    file.close()

    return raw_list
