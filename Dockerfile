FROM python:3.6

RUN pip install gunicorn

RUN mkdir /app
COPY ./Pipfile /app
COPY ./Pipfile.lock /app
WORKDIR /app

RUN pip install pipenv && pipenv install --system

COPY . /app