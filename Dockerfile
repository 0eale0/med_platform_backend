FROM python:3.8

ENV PYTHONUNBUFFERED 1


COPY requirements.txt .
RUN pip install -r requirements.txt && poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY . .

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver
