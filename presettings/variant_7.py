"""Настройки для варианта задания №7у

Поиск пользователей на physics.stackexchange.com, с репутацией не меньше 100,
написавшх как можно больше ответов с 8 утра до 2 часов дня.

"""

# === Режим отладки: ===

debug = False

# === Настройки ввода: ===

# Если файл находится в подкаталоге, укажите относительный путь к нему
users_file_name = 'files/Users.xml'
posts_file_name = 'files/Posts.xml'
in_encoding = 'utf-8'

# === Настройки составления отчета: ===

html_output_file = 'results.html'
# Размер отступов в html-разметке на выходе:
html_spaces = 2
out_encoding = 'utf-8'

# Сайт из Q&A-системы stackexchange (в т. ч. stackoverflow), который парсится
# Необходимо для корректного составления отчета
website = 'physics.stackexchange.com'

# Настройки ограничения вывода
# out_limit_type - тип ограничения
# (0 - без ограничений
#  1 - вывод первых out_limit пользователей,
#  2 - вывод первых out_limit пользователей, а так же пользователей
# с количеством подходящих постов таким же, как у пользователя под номером out_limit
#  3 - вывод пользователей с количеством подходящих постов >= out_limit)
out_limit_type = 2
out_limit = 100

# === Настройки выборки: ===

# Минимальная репутация пользователя.
# Если отбор по этому признаку не требуется, установите крайне малое значение
min_reputation = 100

# Максимальная репутация пользователя (не включительно).
# Если отбор по этому признаку не требуется, установите крайне большое значение
max_reputation = 10 ** 18

# Начальное значение времени (часа) написания, для отбора постов
# Если отбор по этому признаку не требуется, установите 0
min_hour = 8

# Конечное значение времени (часа) написания (не включительно)
# Если отбор по этому признаку не требуется, установите 24
max_hour = 14

# Тип поста: '1' - Вопрос, '2' - Ответ:
post_type = '2'

# Отбирать только ответы, которые были приняты автором вопроса (да - True / нет - False)
# Гарантируется корректная работа только при post_type == '2'
filter_accepted = False
