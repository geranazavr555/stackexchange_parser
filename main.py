"""Главынй файл парсера

Основной исполняемый файл

"""

from time import time

import settings
import parsing
import reporting


def read_raw_xml(filename, encoding_=settings.in_encoding):
    """Читает %filename% в кодировке %_encoding% и возвращает список строк"""

    start_time = time()
    file = open(filename, encoding=encoding_)
    raw_list = file.readlines()
    file.close()

    if settings.debug:
        print('reading "' + filename + '" time (sec):', time() - start_time)

    return raw_list

ts = time()

if settings.debug:
    print('= debug mode on =')

# == Чтение xml ==
users = parsing.parse(read_raw_xml(settings.users_file_name))
posts = parsing.parse(read_raw_xml(settings.posts_file_name))

if settings.debug:
    print('reading and parsing time (sec):', time() - ts)

# ID интересующих нас пользователей:
# И их посты в подходящее время:
interested_users_id = set()
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
user_to_posts_count = dict()

for post in interested_posts:
    if post['OwnerUserId'] in user_to_posts_count:
        user_to_posts_count[post['OwnerUserId']] += 1
    else:
        user_to_posts_count[post['OwnerUserId']] = 1

# Перевод словаря в список для последующей сортировки
raw_output = []
for i in user_to_posts_count:
    raw_output.append((i, user_to_posts_count[i]))
# Убывающая сортировка по количеству постов
raw_output.sort(key=lambda x: x[1], reverse=True)

# == Окончательная запись ответа ==
reporting.gen_html(settings.html_output_file, raw_output)

if settings.debug:
    print('total time (sec):', time() - ts)
