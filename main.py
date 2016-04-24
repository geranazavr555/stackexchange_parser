"""Главынй файл парсера

Основной исполняемый файл

"""

from time import time

from settings import settings
from reading import read_raw_xml
from parsing import parse
from reporting import GenOutput
from filter import filter_posts, filter_users

ts = time()

if settings['debug']:
    print('= debug mode on =')

# == Чтение xml ==
users = parse(read_raw_xml(settings['users_file_name']))
posts = parse(read_raw_xml(settings['posts_file_name']))

if settings['debug']:
    print('reading and parsing time (sec):', time() - ts)
    print('total parsed users:', len(users))
    print('total parsed posts:', len(posts))

interested_posts = filter_posts(posts, filter_users(users))

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
output.generate()
output.writefile()

if settings['debug']:
    print('total time (sec):', time() - ts)
