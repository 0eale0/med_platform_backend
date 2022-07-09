FROM python:3.8

ENV PYTHONUNBUFFERED 1


COPY requirements.txt .
RUN pip install -r requirements.txt && poetry config virtualenvs.create false

WORKDIR /backend
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000

