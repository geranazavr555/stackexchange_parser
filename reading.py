from settings import settings


def read_raw_xml(filename, encoding_=settings['in_encoding']):
    """Читает %filename% в кодировке %_encoding% и возвращает список строк"""

    start_time = time()
    file = open(filename, encoding=encoding_)
    raw_list = file.readlines()
    file.close()

    if settings['debug']:
        print('reading "' + filename + '" time (sec):', time() - start_time)

    return raw_list
