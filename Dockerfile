FROM python:3.9.2

ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY poetry.lock /src/
COPY pyproject.toml /src/
RUN pip install poetry==1.1.8
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . /src/
