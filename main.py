"""Главынй файл парсера

Основной исполняемый файл

"""

from time import time

import settings
import parsing
import reporting

ts = time()

if settings.debug:
    print('= debug mode on =')


def read_raw_xml(filename, _encoding=settings.in_encoding):
    """Читает %filename% в кодировке %_encoding% и возвращает список строк"""
    treads = time()
    file = open(filename, encoding=_encoding)
    raw_list = file.readlines()
    file.close()
    if settings.debug:
        print('reading "' + filename + '" time (sec):', time() - treads)
    return raw_list

# == Чтение xml ==
users = parsing.parse(read_raw_xml(settings.users_file_name))
posts = parsing.parse(read_raw_xml(settings.posts_file_name))

if settings.debug:
    print('reading and parsing time time (sec):', time() - ts)

# ID интересующих нас пользователей:
interested_users_id = set()
# Посты искомых пользователей в подходящее время:
interested_posts = []

# == Выбор пользователей с подходящей репутацией ==
for user in users:
    # Проверка репутации пользователя:
    if settings.min_reputation <= int(user['Reputation']) < settings.max_reputation:
        interested_users_id.add(user['Id'])

# == Выбор постов искомых пользователей в подходящее время ==
for post in posts:
    # Если тип поста подходящий:
    if post['PostTypeId'] == settings.post_type:
        # Если пост написан подходящим пользователем:
        if post.get('OwnerUserId') in interested_users_id:
            # Если пост написан в подходящее время:
            if settings.min_hour <= parsing.get_hour(post['CreationDate']) < settings.max_hour:
                interested_posts.append(post)

if settings.debug:
    print('total parsed users:', len(users))
    print('total parsed posts:', len(posts))
    print('total users that we are interested in:', len(interested_users_id))
    print('total posts, that we are interested in:', len(interested_posts))

# == Предварительная генерация ответа ==

# Словарь {id пользователя : количество постов}
raw_output = dict()
for post in interested_posts:
    if post['OwnerUserId'] in raw_output:
        raw_output[post['OwnerUserId']] += 1
    else:
        raw_output[post['OwnerUserId']] = 1

# == Окончательная запись ответа ==
reporting.gen_html(settings.html_output_file, raw_output)

if settings.debug:
    print('total time (sec):', time() - ts)
