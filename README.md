# back-end part of the med-communication-platform

## Установка и запуск проекта

1) сконфигурировать .env файл исходя из .example.env
2) `python3 -m venv .venv` - создать виртуальное окружение
3) `source .venv/bin/activate` - войти в виртуальное окружение
4) `pip install -r requirements.txt` - установить зависимости ч.1
5) `poetry install` - установить зависимости ч.2
6) `pre-commit install` - установка pre-commit хуков для запуска линтеров перед коммитом
7) `python manage.py migrate` - применить миграции к базе данных
8) `python manage.py runserver` - запуск сервера для разработки
