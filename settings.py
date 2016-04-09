"""
    settings.py
    Файл настроек
"""

# === Режим отладки: ===

debug = True

# === Настройки ввода: ===

users_file_name = 'files/Users.xml'
posts_file_name = 'files/Posts.xml'
in_encoding = 'utf-8'

# === Настройки составления отчета: ===

html_output_file = 'results.html'
html_spaces = 2  # Размер отступов в html-разметке на выходе
out_encoding = 'utf-8'

# === Настройки выборки: ===

min_reputation = 100
# max_reputation =
min_hour = 8
max_hour = 14
post_type = '2'  # Тип поста: '1' - Вопрос, '2' - Ответ

