from time import time

import settings
import parsing
import reporting

ts = time()

if settings.debug:
    print('= debug mode on =')


def read_raw_xml(filename, _encoding=settings.in_encoding):
    treads = time()
    file = open(filename, encoding=_encoding)
    raw_list = file.readlines()
    file.close()
    if settings.debug:
        print('reading "' + filename + '" time (sec):', time() - treads)
    return raw_list

# Чтение xml
users = parsing.parse(read_raw_xml(settings.users_file_name))
posts = parsing.parse(read_raw_xml(settings.posts_file_name))

if settings.debug:
    print('reading and parsing time time (sec):', time() - ts)

interested_users = []  # Интересующие нас пользователи...
interested_users_id = set()  # ... И их id
interested_posts = []  # Посты искомых пользователей в подходящее время

# Выбор пользователей с подходящей репутацией
for user in users:
    if int(user['Reputation']) >= settings.min_reputation:  # Проверка репутации пользователя
        interested_users.append(user)
        interested_users_id.add(user['Id'])

# Выбор постов искомых пользователей в подходящее время
for post in posts:
    if post['PostTypeId'] == settings.post_type:  # Если тип поста подходящий
        if post.get('OwnerUserId') in interested_users_id:  # Если пост написан подходящим пользователем
            # Если пост написан в подходящее время
            if settings.min_hour <= parsing.get_hour(post['CreationDate']) < settings.max_hour:
                interested_posts.append(post)

if settings.debug:
    print('total parsed users:', len(users))
    print('total parsed posts:', len(posts))
    print('total users that we are interested in:', len(interested_users))
    print('total posts, that we are interested in:', len(interested_posts))

# Предварительная генерация ответа
raw_output = dict()  # Словарь {id пользователя : список постов}
for post in interested_posts:
    if post['OwnerUserId'] in raw_output:
        raw_output[post['OwnerUserId']].append(post['Id'])
    else:
        raw_output[post['OwnerUserId']] = [post['Id']]

# Окончательная запись ответа
reporting.gen_html(settings.html_output_file, raw_output)

if settings.debug:
    print('total time (sec):', time() - ts)
