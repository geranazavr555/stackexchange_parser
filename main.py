"""Главынй файл парсера

Основной исполняемый файл

"""

from time import time
from sys import argv
from os.path import isfile

from settings import settings
from reading import read_raw_file
from parsing import parse
from reporting import GenOutput
from filter import filter_posts, filter_users

ts = time()

if len(argv) > 1:
    if argv[1] == '--help':
        if isfile('README.md'):
            for line in read_raw_file('README.md'):
                print(line)
        else:
            print('Смотрите по адресу https://github.com/geranazavr555/stackexchange_parser/README.md')
    else:
        settings.load_from_file(argv[1])

if not settings.validate():
    exit(1)

if settings['debug']:
    print('= debug mode on =')
    print(settings)

# == Чтение xml ==
try:
    users = parse(read_raw_file(settings['users_file_name']))
except IOError:
    print('Невозможно открыть файл ' + settings['users_file_name'] + ' для чтения')
    exit(1)

try:
    posts = parse(read_raw_file(settings['posts_file_name']))
except IOError:
    print('Невозможно открыть файл ' + settings['posts_file_name'] + ' для чтения')
    exit(1)

if settings['debug']:
    print('reading and parsing time (sec):', time() - ts)
    print('total parsed users:', len(users))
    print('total parsed posts:', len(posts))

interested_posts = filter_posts(posts, filter_users(users, settings), settings)

# == Предварительная генерация ответа ==

# Словарь {id пользователя : количество постов}
user_to_posts_count = dict()

for post in interested_posts:
    if post['OwnerUserId'] in user_to_posts_count:
        user_to_posts_count[post['OwnerUserId']] += 1
    else:
        user_to_posts_count[post['OwnerUserId']] = 1

# Перевод словаря в список для последующей сортировки
raw_output = [item for item in user_to_posts_count.items()]

# Убывающая сортировка по количеству постов
raw_output.sort(key=lambda x: x[1], reverse=True)

# == Окончательная запись ответа ==
output = GenOutput(raw_output)
output.settings = settings
output.generate()
output.writefile()

if settings['debug']:
    print('total time (sec):', time() - ts)
