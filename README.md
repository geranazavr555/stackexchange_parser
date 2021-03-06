# Stackexchange parser

Вступительная работа в ЛКШ-2016.P v2.0

Автор: Назаров Георгий, г. Ставрополь

### Отличия от v1.1.1
* Переработана система настроек
* Убрана сильная связность модулей
* Добавлена функция вывода настроек парсинга в отчет
* Добавлена защита от ошибок
* Увеличина читаемость кода

## Что делает?

Скрипт отбирает пользователей какого-либо из сайтов группы stackexchange, имеющих заданную репутацию, написавшие как можно больше постов в заданое время.
Возможен отбор ответов, которые были помечены автором вопроса.

## Использование

main.py [--help] [settings-file-name]

##### Описание аргументов
* --help - выводит README
* settings-file-name - задаёт файл настроек. По умолчанию используется default.cfg

Автор рекомендует запускть в интерпретаторе PyPy, но это не является обязательным условием работы. (Можете запускать в любом интерпретаторе, поддерживающем Python 3.5.1, на ваше усмотрение)

## Настройки

Все настройки содержатся в файле settings.py

**Обратите внимание!**
В подкаталоге *"/presettings/"* содержатся конфигурации для таких случаев:

* Вариант вступительной №7: файл */presettings/variant_7.cfg*
* Вариант вступительной №7у: файл */presettings/variant_7u.cfg*

При использовании какого-либо из этих вариантов конфигурации, просто запустите main.py, передав в качестве аргумента коммандной строки относительный адрес нужной конфигурации.

**Настройки по умолчанию:**
Вариант 7у
* Репутация пользователей: от 100 и более
* Тип поста: ответ, который был помечен автором вопроса
* Вывод пользователей, имеющих количество подходящих постов не меньше, чем у пользователя на 100 месте в сортировке по убыванию

По умолчанию Users.xml и Posts.xml должны находится в подкаталоге *"/files/"*

##### Описание настроек

* _users_file_name_ - относительный путь к файлу с пользователями
* _posts_file_name_ - относительный пусть к файлу с постами
* _html_output_file_ - имя выходного файла. Если не указано, то название формируется используя текущую дату и время
* _generate_css_ - генерировать ли оформление отчета (1 - да, 0 - нет)
* _generate_header_ - генерировать ли заголовок и дополнительную информацию в отчёте
* _website_ - сайт, который парсится
* _min_reputation_ - минимальная репутация пользователя
* _max_reputation_ - максимальная репутация пользователя (не включительно)
* _min_hour_ - начальное значение часа, когда должен был быть написан пост
* _max_hour_ - конечное значение часа (не включительно), когда должен был быть написан пост
* _post_type_ - тип отбираемых постов. (1 - Вопрос, 2 - Ответ)
* _filter_accepted_ - Отбирать ли только ответы, принятые автором поста (1 - да, 0 - нет)
* _out_limit_type_ - тип ограничения вывода (0 - без ограничений, 1 - вывод первых _out_limit_ пользователей, 2 - вывод пользователей, имеющих количество подходящих постов, не менее, чем у пользователя под номером _out_limit_, 3 - вывод пользователей, имеющих количество подходящих постов не менне _out_limit_)
* _out_limit_ - см. _out_limit_type_