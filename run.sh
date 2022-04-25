export $(cat .env)
./.heroku/python/bin/poetry config virtualenvs.create false
./.heroku/python/bin/poetry install --no-dev
./.heroku/python/bin/python manage.py migrate
./.heroku/python/bin/python manage.py collectstatic
./.heroku/python/bin/gunicorn med_communication_platform.wsgi
./.heroku/python/bin/celery -A med_communication_platform worker -l INFO
