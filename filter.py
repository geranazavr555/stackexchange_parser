

def get_hour(datetime):
    """Выделяет из строки вида yyyy-mm-ddThh-mm-ss.sss часы"""
    return int(datetime[datetime.find('T') + 1:datetime.find(':')])


def filter_users(users, settings):
    interested_users_id = set()
    # == Выбор пользователей с подходящей репутацией ==
    for user in users:
        # Проверка репутации пользователя:
        if settings['min_reputation'] <= int(user['Reputation']) < settings['max_reputation']:
            interested_users_id.add(user['Id'])
    return interested_users_id


def filter_posts(posts, interested_users_id, settings):
    # ID постов, которые были помечены, как "Ответ"
    accepted_answers_id = set()

    # Если необходимо, поиск ответов, которые были помечены автором вопроса
    if settings['filter_accepted']:
        for post in posts:
            accepted_answers_id.add(post.get('AcceptedAnswerId'))

    interested_posts = []
    # == Выбор постов искомых пользователей в подходящее время ==
    for post in posts:
        # Если тип поста подходящий:
        if post['PostTypeId'] == settings['post_type']:
            # Если пост написан подходящим пользователем:
            if post.get('OwnerUserId') in interested_users_id:
                # Если пост написан в подходящее время:
                if settings['min_hour'] <= get_hour(post['CreationDate']) < settings['max_hour']:
                    # Если необходимо, отбор ответов, помеченых автором вопроса
                    if settings['filter_accepted']:
                        if post['Id'] in accepted_answers_id:
                            interested_posts.append(post)
                    else:
                        interested_posts.append(post)
    return interested_posts
