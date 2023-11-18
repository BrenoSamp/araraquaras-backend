FROM python:3.9
LABEL maintainer='Brenim'

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install -r requirements.txt

ENV PATH="/py/bin:$PATH"

EXPOSE 8000