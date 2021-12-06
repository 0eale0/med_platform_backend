# shellcheck disable=SC2046
export $(xargs <.env)
/app/.heroku/python/bin/python -m pip install --upgrade pip
./.heroku/python/bin/poetry config virtualenvs.create false
./.heroku/python/bin/poetry install --no-dev
./.heroku/python/bin/python manage.py migrate
./.heroku/python/bin/python manage.py collectstatic
./.heroku/python/bin/gunicorn med_communication_platform.wsgi