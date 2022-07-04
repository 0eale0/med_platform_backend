FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /backend
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pyproject.toml .
COPY poetry.lock .
COPY .pre-commit-config.yaml .
RUN poetry install
RUN pre-commit install

COPY . .

EXPOSE 8000

